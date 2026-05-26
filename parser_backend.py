# parser_backend.py

KEYWORDS = ["int", "float", "double", "char", "string", "if", "else", "while", "for", "return", "print", "read", "true", "false", "bool"]
OPERATORS = ["=", "+", "-", "*", "/", "<", ">", "<=", ">=", "==", "!=", "&&", "||", "%", "!", "++", "--"]
SEPARATORS = [";", ",", "(", ")", "{", "}"]

class Token:
    def __init__(self, value, category, line_num, raw_line):
        self.value = value
        self.category = category
        self.line_num = line_num
        self.raw_line = raw_line

def generate_token_stream(content):
    tokens = []
    lines = content.splitlines()
    multi_line_comment = False

    for line_num, raw_line in enumerate(lines, 1):
        line = raw_line
        
        # Handle Comments
        if multi_line_comment:
            if "*/" in line:
                line = line.split("*/", 1)[1]
                multi_line_comment = False
            else: continue
                
        if "/*" in line:
            if "*/" in line:
                parts = line.split("/*", 1)
                after = parts[1].split("*/", 1)[1]
                line = parts[0] + " " + after
            else:
                line = line.split("/*", 1)[0]
                multi_line_comment = True
                
        if "//" in line: line = line.split("//", 1)[0]

        # Token Extraction
        words = []
        temp = ""
        in_string = False
        in_char = False
        i = 0
        
        while i < len(line):
            char = line[i]
            if (in_string or in_char) and char == '\\':
                temp += char; i += 1
                if i < len(line): temp += line[i]
                i += 1; continue
                
            if char == '"' and not in_char:
                in_string = not in_string
                temp += char
                if not in_string: words.append(temp); temp = ""
            elif in_string: temp += char
            elif char == "'" and not in_string:
                in_char = not in_char
                temp += char
                if not in_char: words.append(temp); temp = ""
            elif in_char: temp += char
            elif i + 1 < len(line) and line[i:i+2] in ["==", "!=", "<=", ">=", "&&", "||", "++", "--"]:
                if temp: words.append(temp)
                words.append(line[i:i+2])
                temp = ""; i += 1
            elif char in SEPARATORS or char in OPERATORS:
                if temp: words.append(temp)
                words.append(char)
                temp = ""
            elif char.isspace():
                if temp: words.append(temp); temp = ""
            else: temp += char
            i += 1
            
        if temp: words.append(temp)

        # Categorize
        for w in words:
            if w in KEYWORDS: cat = "KEYWORD"
            elif w in SEPARATORS: cat = "SEPARATOR"
            elif w in OPERATORS: cat = "OPERATOR"
            elif w.isdigit() or ('.' in w and w.replace('.','',1).isdigit()) or w.startswith('"') or w.startswith("'"): cat = "LITERAL"
            else: cat = "IDENTIFIER"
            tokens.append(Token(w, cat, line_num, raw_line.strip()))
            
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []
        self.scope_depth = 0
        self.data_types = ["int", "float", "double", "char", "string", "bool", "void"]

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def peek(self):
        return self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None

    def advance(self):
        if self.pos < len(self.tokens): self.pos += 1

    def match(self, expected_value):
        tok = self.current()
        if tok and tok.value == expected_value:
            if expected_value == "{": self.scope_depth += 1
            if expected_value == "}": self.scope_depth -= 1
            self.advance()
            return True
        return False

    def report_error(self, err_type, message, use_prev=False):
        tok = self.tokens[self.pos - 1] if use_prev and self.pos > 0 else self.current()
        if tok:
            self.errors.append({"line": tok.line_num, "type": err_type, "message": message, "code": tok.raw_line})
        else:
            prev = self.tokens[-1] if self.tokens else None
            line = prev.line_num if prev else 0
            self.errors.append({"line": line, "type": err_type, "message": message, "code": "End of File"})

    def sync(self):
        while self.current():
            val = self.current().value
            if val in [";", "}"]:
                self.advance()
                return
            if val in self.data_types or val in ["if", "while", "for", "return", "print", "read"]:
                return
            self.advance()

    def parse(self):
        while self.current():
            if not self.parse_statement():
                self.advance()
        
        if self.scope_depth > 0:
            self.report_error("Missing Brace", "Missing closing brace '}' at end of file.", use_prev=True)

    def parse_statement(self):
        tok = self.current()
        if not tok: return False

        if tok.value in self.data_types:
            if self.peek() and self.peek().value == "main": self.parse_main_function()
            else: self.parse_declaration()
            return True
        elif tok.value == "if":
            self.parse_if_statement()
            return True
        elif tok.value == "else":
            self.advance()
            if self.current() and self.current().value == "if": pass 
            elif not self.match("{"): self.report_error("Syntax Error", "Expected '{' after else.")
            return True
        elif tok.value == "while":
            self.parse_while_statement()
            return True
        elif tok.value == "for":
            self.parse_for_statement()
            return True
        elif tok.value in ["print", "read"]:
            self.parse_io_statement()
            return True
        elif tok.category == "IDENTIFIER":
            self.parse_assignment()
            return True
        elif tok.value in ["{", "}"]:
            self.match(tok.value) 
            return True
        elif tok.value == "return":
            self.advance()
            self.parse_expression()
            if not self.match(";"): self.report_error("Missing Semicolon", "Expected ';' after return statement.", use_prev=True)
            return True
        else:
            self.report_error("Syntax Error", f"Unexpected token '{tok.value}'.")
            self.sync()
            return True

    def parse_main_function(self):
        self.advance() 
        self.advance() 
        if not self.match("("): self.report_error("Syntax Error", "Expected '(' after main.")
        if not self.match(")"): self.report_error("Syntax Error", "Expected ')' after main(.", use_prev=True)
        if not self.match("{"): self.report_error("Syntax Error", "Expected '{' to start main body.")

    def parse_declaration(self):
        self.advance() 
        while True:
            tok = self.current()
            if not tok or tok.category != "IDENTIFIER":
                self.report_error("Invalid Declaration", "Expected identifier after data type.")
                self.advance() # FORCE ADVANCE to break the loop!
                self.sync() 
                return

            self.advance() 
            if self.match("="): self.parse_expression()
            
            if self.match(","): continue
            else: break
                
        if not self.match(";"):
            self.report_error("Missing Semicolon", "Expected ';' at the end of declaration.", use_prev=True)
            self.sync()

    def parse_assignment(self):
        self.advance() 
        if self.match("="):
            self.parse_expression()
            if not self.match(";"):
                self.report_error("Missing Semicolon", "Expected ';' at the end of assignment.", use_prev=True)
                self.sync()
        elif self.match("++") or self.match("--"):
            if not self.match(";"):
                self.report_error("Missing Semicolon", "Expected ';' after increment/decrement.", use_prev=True)
                self.sync()
        else:
            self.report_error("Invalid Assignment", "Expected '=' after identifier.")
            self.sync()

    def parse_if_statement(self):
        self.advance() 
        if not self.match("("): self.report_error("Syntax Error", "Expected '(' after 'if'.")
        self.parse_expression()
        if not self.match(")"): self.report_error("Mismatched Parenthesis", "Expected ')' to close if condition.", use_prev=True)
        if not self.match("{"): self.report_error("Syntax Error", "Expected '{' to start if body.")

    def parse_while_statement(self):
        self.advance() 
        if not self.match("("): self.report_error("Syntax Error", "Expected '(' after 'while'.")
        self.parse_expression()
        if not self.match(")"): self.report_error("Mismatched Parenthesis", "Expected ')' to close while condition.", use_prev=True)
        if not self.match("{"): self.report_error("Syntax Error", "Expected '{' to start while body.")

    def parse_for_statement(self):
        self.advance() 
        if not self.match("("): self.report_error("Syntax Error", "Expected '(' after 'for'.")
        
        # Init
        if self.current() and self.current().value in self.data_types:
            self.advance(); self.advance()
            if self.match("="): self.parse_expression()
        else:
            self.advance()
            if self.match("="): self.parse_expression()
            
        if not self.match(";"): self.report_error("Missing Semicolon", "Expected ';' after for initialization.", use_prev=True)
        
        # Cond
        self.parse_expression()
        if not self.match(";"): self.report_error("Missing Semicolon", "Expected ';' after for condition.", use_prev=True)
        
        # Update
        self.parse_expression()
        if not self.match(")"): self.report_error("Mismatched Parenthesis", "Expected ')' to close for loop.", use_prev=True)
        if not self.match("{"): self.report_error("Syntax Error", "Expected '{' to start for body.")

    def parse_io_statement(self):
        self.advance() 
        self.parse_expression()
        if not self.match(";"): self.report_error("Missing Semicolon", "Expected ';' after IO statement.", use_prev=True)

    def parse_expression(self):
        paren_count = 0
        first_token = True
        last_was_operand = False 
        last_was_operator = False
        
        while self.current():
            c_tok = self.current()
            
            if first_token and c_tok.category == "OPERATOR" and c_tok.value not in ["!", "++", "--"]:
                self.report_error("Invalid Expression", f"Expression cannot start with binary operator '{c_tok.value}'.")
                self.advance()
                first_token = False
                last_was_operator = True
                continue
                
            first_token = False
            
            if c_tok.value == "(":
                paren_count += 1
                self.advance()
                last_was_operand = False
                last_was_operator = False
            elif c_tok.value == ")":
                if paren_count > 0:
                    paren_count -= 1
                    self.advance()
                    last_was_operand = True
                    last_was_operator = False
                else: break
            elif c_tok.category in ["IDENTIFIER", "LITERAL"] or c_tok.value in ["true", "false"]:
                if last_was_operand: break 
                last_was_operand = True
                last_was_operator = False
                self.advance()
            elif c_tok.category == "OPERATOR":
                # Catch the back-to-back operators like '+ *' here!
                if last_was_operator and c_tok.value not in ["!", "++", "--"]:
                    self.report_error("Invalid Expression", f"Unexpected consecutive operator '{c_tok.value}'.")
                last_was_operator = True
                last_was_operand = False
                self.advance()
            else:
                break
                
        if paren_count > 0: self.report_error("Mismatched Parenthesis", "Unclosed '(' in expression.", use_prev=True)

def run_syntax_analyzer(content):
    tokens = generate_token_stream(content)
    parser = Parser(tokens)
    parser.parse()
    
    return {
        "success": len(parser.errors) == 0,
        "errors": parser.errors
    }