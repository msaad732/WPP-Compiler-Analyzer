# The Rule Book
KEYWORDS = ["int", "float", "double", "char", "string", "if", "else", "while", "for", "return", "print", "read", "true", "false", "bool"]
OPERATORS = ["=", "+", "-", "*", "/", "<", ">", "<=", ">=", "==", "!=", "&&", "||", "%", "!", "++", "--"]  # FIX 1: Added ++ and --
SEPARATORS = [";", ",", "(", ")", "{", "}"]

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
        "!=": "NEQ", "&&": "AND", "||": "OR", "%": "MOD", "!": "NOT",
        "++": "INCREMENT", "--": "DECREMENT"  # FIX 1 (cont): Named entries for ++ and --
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

    all_lines = content.splitlines()
    total_lines_count = len(all_lines)

    # FIX 2: Renamed loop variable from 'content' to 'raw_line' to avoid shadowing the parameter
    for line_number, raw_line in enumerate(all_lines, 1):
        line = raw_line  # work on a mutable copy

        if multi_line_comment:
            if "*/" in line:
                line = line.split("*/", 1)[1]
                multi_line_comment = False
            else:
                continue

        if "/*" in line:
            if "*/" in line:
                parts = line.split("/*", 1)
                after_part = parts[1].split("*/", 1)[1]
                line = parts[0] + " " + after_part
            else:
                line = line.split("/*", 1)[0]
                multi_line_comment = True

        if "//" in line:
            line = line.split("//", 1)[0]

        words = []
        temp_word = ""
        in_string = False
        in_char = False

        i = 0
        while i < len(line):
            char = line[i]

            if char == '"' and not in_char:
                in_string = not in_string
                temp_word += char
                if not in_string:
                    words.append(temp_word); temp_word = ""
            elif in_string:
                temp_word += char

            elif char == "'" and not in_string:
                in_char = not in_char
                temp_word += char
                if not in_char:
                    words.append(temp_word); temp_word = ""
            elif in_char:
                temp_word += char

            # FIX 1 (cont): Check ++ and -- BEFORE single + and - so they don't split
            elif i + 1 < len(line) and line[i:i+2] in ["==", "!=", "<=", ">=", "&&", "||", "++", "--"]:
                if temp_word: words.append(temp_word)
                words.append(line[i:i+2])
                temp_word = ""; i += 1

            elif char in SEPARATORS or char in OPERATORS:
                if temp_word: words.append(temp_word)
                words.append(char)
                temp_word = ""

            elif char.isspace():
                if temp_word: words.append(temp_word); temp_word = ""
            else:
                temp_word += char
            i += 1

        if temp_word: words.append(temp_word)

        if words:
            lines_with_code += 1
            line_distribution[line_number] = len(words)

            for word in words:
                total_tokens += 1

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

                stats[cat] += 1
                token_lines[cat].append(line_number)

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

    # Analytics
    unique_token_types = len(detailed_stats)

    # FIX 3: Use total_lines_count instead of bare 'line_number' (which would crash on empty files)
    empty_lines = total_lines_count - lines_with_code

    most_frequent_type = max(stats, key=stats.get) if any(stats.values()) else "N/A"
    least_frequent_type = min(stats, key=stats.get) if any(stats.values()) else "N/A"

    avg_tokens = round(total_tokens / lines_with_code, 2) if lines_with_code > 0 else 0

    if line_distribution:
        max_tokens_count = max(line_distribution.values())
        min_tokens_count = min(line_distribution.values())
        max_line = max(line_distribution, key=line_distribution.get)
        min_line = min(line_distribution, key=line_distribution.get)
    else:
        max_tokens_count = 0
        min_tokens_count = 0
        max_line = 0
        min_line = 0

    return {
        "stats": stats,
        "detailed_stats": detailed_stats,
        "detailed_lines": detailed_lines,
        "total_tokens": total_tokens,
        "lines_with_code": lines_with_code,
        "total_lines": total_lines_count,
        "line_distribution": line_distribution,
        "identifier_details": identifier_details,
        "literal_types": literal_types,
        "literal_lines": literal_lines,
        # FIX 4: Analytics were computed but never returned — now included
        "analytics": {
            "unique_token_types": unique_token_types,
            "empty_lines": empty_lines,
            "most_frequent_type": most_frequent_type,
            "least_frequent_type": least_frequent_type,
            "avg_tokens_per_line": avg_tokens,
            "densest_line": max_line,
            "densest_line_token_count": max_tokens_count,
            "sparsest_line": min_line,
            "sparsest_line_token_count": min_tokens_count,
        }
    }
