# The Rule Book
KEYWORDS = ["int", "float", "double", "char", "string", "if", "else", "while", "for", "return", "print", "read", "true", "false","bool"]
OPERATORS = ["=", "+", "-", "*", "/", "<", ">", "<=", ">=", "==", "!=", "&&", "||","%","!"]
SEPARATORS = [";", ",", "(", ")", "{", "}"]

# Our "Tally Sheet" to count things
def run_token_analyzer(content):
    stats = {
        "KEYWORD": 0,
        "SEPARATOR": 0,
        "OPERATOR": 0,
        "LITERAL": 0,
        "IDENTIFIER": 0
    }

    token_lines = {
        "KEYWORD": [],
        "SEPARATOR": [],
        "OPERATOR": [],
        "LITERAL": [],
        "IDENTIFIER": []
    }

    operator_names = {
        "=": "ASSIGN", "+": "PLUS", "-": "MINUS", "*": "MULT", "/": "DIV",
        "<": "LT", ">": "GT", "<=": "LTE", ">=": "GTE", "==": "EQ",
        "!=": "NEQ", "&&": "AND", "||": "OR","%": "MOD", "!": "NOT"
    }

    separator_names = {
        ";": "SEMICOLON", ",": "COMMA", "(": "LPAREN", ")": "RPAREN",
        "{": "LBRACE", "}": "RBRACE"
    }

    detailed_stats = {}
    detailed_lines = {}

    total_tokens = 0
    lines_with_code = 0


    line_distribution = {}
    identifier_details = {}
    literal_types = {} 
    literal_lines = {}

    multi_line_comment = False
    # This opens the test file
    # file_name = "test1.wpp"

    all_lines = content.splitlines()
    total_lines_count = len(all_lines)
    
    for line_number, content in enumerate(all_lines, 1):
        #checks if comment and valid code is on the same line, if so it will ignore the comment and only analyze the code
        if multi_line_comment:
            if "*/" in content:
                content = content.split("*/", 1)[1]
                multi_line_comment = False
            else:
                continue
        #for multi-line comments
        if "/*" in content:
            if "*/" in content:
                parts = content.split("/*", 1)
                after_part = parts[1].split("*/", 1)[1]
                content = parts[0] + " " + after_part
            else:
                content = content.split("/*", 1)[0]
                multi_line_comment = True
        #for single-line comments
        if "//" in content:
            content = content.split("//", 1)[0]
    #For literals or strings
        words = []
        temp_word = ""
        in_string = False
        in_char = False

        i = 0
        while i < len(content):
            char = content[i]
            
            # Keeps string as single token
            if char == '"' and not in_char:
                in_string = not in_string
                temp_word += char
                if not in_string: 
                    words.append(temp_word); temp_word = ""
            elif in_string:
                temp_word += char
            
            # For character literals
            elif char == "'" and not in_string:
                in_char = not in_char
                temp_word += char
                if not in_char:
                    words.append(temp_word); temp_word = ""
            elif in_char:
                temp_word += char

            # For multi-char operators like &&, ||, <=, >= 
            elif i + 1 < len(content) and content[i:i+2] in ["==", "!=", "<=", ">=", "&&", "||"]:
                if temp_word: words.append(temp_word)
                words.append(content[i:i+2])
                temp_word = ""; i += 1 
            
            # Handles separators and single operators
            elif char in SEPARATORS or char in OPERATORS:
                if temp_word: words.append(temp_word)
                words.append(char)
                temp_word = ""
            
            # For whitespace 
            elif char.isspace():
                if temp_word: words.append(temp_word); temp_word = ""
            else:
                temp_word += char
            i += 1
        
        if temp_word: words.append(temp_word)

        if words: # This checks if the line actually has words (not just an empty line)
            lines_with_code += 1
            line_distribution[line_number] = len(words)

            for word in words:
                total_tokens += 1 # Every word we find adds to the total count
            
                # Determine l_type for literals first
                l_type = None
                if word.isdigit():
                    l_type = "INTEGER"
                elif "." in word and word.replace(".", "", 1).isdigit():
                    l_type = "FLOAT"
                elif word.startswith("'") and word.endswith("'"):
                    l_type = "CHAR"
                elif word.startswith('"') and word.endswith('"'):
                    l_type = "STRING"

                if word in KEYWORDS:
                    cat = "KEYWORD"
                    tok_type = "KEYWORD_" + word.upper()
                elif word in SEPARATORS:
                    cat = "SEPARATOR"
                    tok_type = "SEPARATOR_" + separator_names.get(word, "UNKNOWN")
                elif word in OPERATORS:
                    cat = "OPERATOR"
                    tok_type = "OPERATOR_" + operator_names.get(word, "UNKNOWN")
                elif l_type:
                    cat = "LITERAL"
                    tok_type = "LITERAL_" + l_type
                else:
                    cat = "IDENTIFIER"
                    tok_type = "IDENTIFIER"

                # Update general stats
                stats[cat] += 1
                token_lines[cat].append(line_number)

                # Update detailed stats
                key = (cat, tok_type)
                if key not in detailed_stats:
                    detailed_stats[key] = 0
                    detailed_lines[key] = []
                detailed_stats[key] += 1
                detailed_lines[key].append(line_number)

                if cat == "IDENTIFIER":
                    if word not in identifier_details:
                        identifier_details[word] = []
                    identifier_details[word].append(line_number)

                if cat == "LITERAL":
                    literal_types[word] = l_type
                    if word not in literal_lines:
                        literal_lines[word] = []
                    literal_lines[word].append(line_number)

    # 1. Basic Counts
    unique_token_types = len(detailed_stats) # Counts how many categories we have
    empty_lines = line_number - lines_with_code # Total lines minus lines with code 

    # 2. Find Most and Least Frequent 
    # We look at our 'stats' dictionary to find the highest and lowest numbers
    most_frequent_type = max(stats, key=stats.get)
    least_frequent_type = min(stats, key=stats.get)

    # 3. Calculate Average 
    if lines_with_code > 0:
        avg_tokens = total_tokens / lines_with_code
    else:
        avg_tokens = 0

    if line_distribution:
        max_tokens_count = max(line_distribution.values())
        min_tokens_count = min(line_distribution.values())
        
        # Optional: Find which line numbers had these counts
        max_line = max(line_distribution, key=line_distribution.get)
        min_line = min(line_distribution, key=line_distribution.get)
    else:
        max_tokens_count = 0
        min_tokens_count = 0

    return {
        "stats": stats,
        "detailed_stats": detailed_stats, 
        "detailed_lines": detailed_lines,
        "total_tokens": total_tokens, 
        "lines_with_code": lines_with_code, 
        "total_lines": len(all_lines),
        "line_distribution": line_distribution, 
        "identifier_details": identifier_details,
        "literal_types": literal_types, 
        "literal_lines": literal_lines
    }


    