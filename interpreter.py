#!/usr/bin/python3
import sys
import math

KEYWORDS = [
    "ADD", "SUB",
    "MUL", "DIV",
    "SIN", "COS",
    "TAN"
]

add = lambda l, vars: int(get_var(l[1], vars))+int(get_var(l[2], vars))
sub = lambda l, vars: int(get_var(l[1], vars))-int(get_var(l[2], vars))
mul = lambda l, vars: int(get_var(l[1], vars))*int(get_var(l[2], vars))
div = lambda l, vars: int(get_var(l[1], vars))/int(get_var(l[2], vars))
sine = lambda l, vars: math.sin(int(get_var(l[1], vars)))
cosine = lambda l, vars: math.cos(int(get_var(l[1], vars)))
tangent = lambda l, vars: math.tan(int(get_var(l[1], vars)))

# This function allows us to write less code in order
# to handle a line and call their respective functions.
def handle_line(line, variables, func, num_args, lines, assign=False):
    check_bounds(line, num_args, lines)
    result = func(line, variables)
    if assign:
        return result
    print(result)

# This function makes sure that enough arguments
# are passed to the interpreter allowing us to
# avoid crashing the interpreter. `n` is the
# number of expected arguments for the keyword.
def check_bounds(line, n, lines):
    if line[0] == "SET" and line[2] in KEYWORDS:
        if len(line) < 5:
            print(f"error: not enough arguments on line {lines}")
            sys.exit(1)
    else:
        try:
            _ = line[n]
        except IndexError:
            print(f"error: not enough arguments on line {lines}")
            sys.exit(1)

# This function retrieves variables if they exist,
# else they return the passed keyword back to the program.
def get_var(keyword, variables):
    if keyword in variables:
        return variables[keyword]
    return keyword

# This function interprets our language code and ultimately runs it.
def interpret(code):
    lines = code.splitlines()
    variables = {}
    labels = {} # Labels allow GOTO statements for loops.

    # First, we collect labels
    for i, line in enumerate(lines):
        parts = line.split()
        if parts and parts[0] == "LABEL":
            labels[parts[1]] = i # Add label and line numner

    # Next, we run the interpreter like normal
    program_counter = 0
    while program_counter < len(lines):
        line = lines[program_counter].split()

        # Empty line
        if not line:
            program_counter += 1
            continue
        
        match line[0]:
            case "ADD": handle_line(line, variables, add, 2, program_counter+1)
            case "SUB": handle_line(line, variables, sub, 2, program_counter+1)
            case "MUL": handle_line(line, variables, mul, 2, program_counter+1)
            case "DIV":
                if line[2] == "0":
                    print(f"error: div by zero on line {program_counter+1}")
                else:
                    handle_line(line, variables, div, 2, program_counter+1)
            case "SIN": handle_line(line, variables, sine, 1, program_counter+1)
            case "COS": handle_line(line, variables, cosine, 1, program_counter+1)
            case "TAN": handle_line(line, variables, tangent, 1, program_counter+1)
            case "SET":
                if len(line) > 2 and line[2] in KEYWORDS:
                    args = line[2:]
                    match line[2]:
                        case "ADD":
                            variables[line[1]] = handle_line(args, variables, add, 2, program_counter+1, assign=True)
                        case "SUB":
                            variables[line[1]] = handle_line(args, variables, sub, 2, program_counter+1, assign=True)
                        case "MUL":
                            variables[line[1]] = handle_line(args, variables, mul, 2, program_counter+1, assign=True)
                        case "DIV":
                            if line[2] == "0":
                                print(f"error: div by zero on line {program_counter+1}")
                            else:
                                variables[line[1]] = handle_line(args, variables, div, 2, program_counter+1, assign=True)
                        case "SIN":
                            variables[line[1]] = handle_line(args, variables, sine, 1, program_counter+1, assign=True)
                        case "COS":
                            variables[line[1]] = handle_line(args, variables, cosine, 1, program_counter+1, assign=True)
                        case "TAN":
                            variables[line[1]] = handle_line(args, variables, tangent, 1, program_counter+1, assign=True)
                else:
                    variables[line[1]] = get_var(line[2], variables)
            # Skip LABEL
            case "GOTO":
                program_counter = labels[line[1]]
                continue # We want to jump straight to the LABEL location
            case "IFGOTO":
                # If ____ ____ Then Go To ____
                if str(get_var(line[1], variables)) == line[2]:
                    program_counter = labels[line[3]]
                    continue # Same as GOTO
            case "PRINT":
                print(get_var(line[1], variables))
        program_counter += 1

def main():
    if len(sys.argv) < 2:
        print("Loading REPL...")
        print("Type 'exit' or 'quit' to exit.")
        try:
            while True:
                line = input(">>> ")
                if line.strip() in ["exit", "quit"]:
                    break
                interpret(line)
        except KeyboardInterrupt:
            sys.exit(0)
    else:
        interpret(open(sys.argv[1], 'r').read())

if __name__ == "__main__":
    main()
