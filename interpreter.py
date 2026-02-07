#!/usr/bin/python3
import sys
import math

add = lambda l: int(l[1])+int(l[2])
sub = lambda l: int(l[1])-int(l[2])
mul = lambda l: int(l[1])*int(l[2])
div = lambda l: int(l[1])/int(l[2])
sine = lambda l: math.sin(int(l[1]))
cosine = lambda l: math.cos(int(l[1]))
tangent = lambda l: math.tan(int(l[1]))

# This function allows us to write less code in order
# to handle a line and call their respective functions.
def handle_line(line, func, num_args, lines):
    check_bounds(line, num_args, lines)
    print(func(line))

# This function makes sure that enough arguments
# are passed to the interpreter allowing us to
# avoid crashing the interpreter. `n` is the
# number of expected arguments for the keyword.
def check_bounds(line, n, lines):
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
    # TODO

    # Next, we run the interpreter like normal
    for line in code.splitlines():
        lines += 1
        line = line.split()
        match line[0]:
            case "ADD": handle_line(line, add, 2, lines)
            case "SUB": handle_line(line, sub, 2, lines)
            case "MUL": handle_line(line, mul, 2, lines)
            case "DIV":
                if line[2] == "0":
                    print(f"error: div by zero on line {lines}")
                else:
                    handle_line(line, div, 2, lines)
            case "SIN": handle_line(line, sine, 1, lines)
            case "COS": handle_line(line, cosine, 1, lines)
            case "TAN": handle_line(line, tangent, 1, lines)

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
