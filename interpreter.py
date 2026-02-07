#!/usr/bin/python3
import sys
import math


def add(args, vars):
    return int(get_var(args[0], vars)) + int(get_var(args[1], vars))


def sub(args, vars):
    return int(get_var(args[0], vars)) - int(get_var(args[1], vars))


def mul(args, vars):
    return int(get_var(args[0], vars)) * int(get_var(args[1], vars))


def div(args, vars):
    return int(get_var(args[0], vars)) / int(get_var(args[1], vars))


def sine(args, vars):
    return math.sin(int(get_var(args[0], vars)))


def cosine(args, vars):
    return math.cos(int(get_var(args[0], vars)))


def tangent(args, vars):
    return math.tan(int(get_var(args[0], vars)))


KEYWORDS = ["ADD", "SUB", "MUL", "DIV", "SIN", "COS", "TAN"]
OPERATION_MAP = {
    "ADD": (add, 2),
    "SUB": (sub, 2),
    "MUL": (mul, 2),
    "DIV": (div, 2),
    "SIN": (sine, 1),
    "COS": (cosine, 1),
    "TAN": (tangent, 1),
}


def check_bounds(args, n, lines):
    """
    This function makes sure that enough arguments
    are passed to the interpreter allowing us to
    avoid crashing the interpreter. `n` is the
    number of expected arguments for the keyword.
    """
    if len(args) < n:
        print(f"error: not enough arguments on line {lines}")
        sys.exit(1)


def get_var(keyword, variables):
    """
    This function retrieves variables if they exist,
    else they return the passed keyword back to the program.
    """
    if keyword in variables:
        return variables[keyword]
    return keyword


def handle_line(args, variables, func, num_args, lines):
    """
    This function allows us to write less code in order
    to handle arguments and call their respective functions.
    """
    check_bounds(args, num_args, lines)
    return func(args, variables)


def handle_set(line, variables, program_counter):
    var_name = line[1]
    if len(line) > 2 and line[2] in OPERATION_MAP:
        operation, num_args = OPERATION_MAP[line[2]]
        args = line[3:]
        if line[2] == "DIV" and get_var(args[2], variables) == "0":
            print(f"error: div by zero on line {program_counter + 1}")
            sys.exit(1)
        variables[var_name] = handle_line(
            args, variables, operation, num_args, program_counter + 1
        )
    else:
        variables[var_name] = get_var(line[2], variables)
    return variables, program_counter


def interpret(code):
    """This function interprets our language code and ultimately runs it."""
    lines = code.splitlines()
    variables = {}
    labels = {}  # Labels allow GOTO statements for loops.

    # First, we collect labels
    for i, line in enumerate(lines):
        parts = line.split()
        if parts and parts[0] == "LABEL":
            labels[parts[1]] = i  # Add label and line number

    # Next, we run the interpreter like normal
    program_counter = 0
    while program_counter < len(lines):
        line = lines[program_counter].split()

        # Empty line
        if not line:
            program_counter += 1
            continue

        match line[0]:
            case "SET":
                variables, program_counter = handle_set(
                    line, variables, program_counter
                )
            case "GOTO":
                program_counter = labels[line[1]]
                continue  # We want to jump straight to the LABEL location
            case "IFGOTO":
                # If ____ ____ Then Go To ____
                if str(get_var(line[1], variables)) == line[2]:
                    program_counter = labels[line[3]]
                    continue  # Same as GOTO
            case "PRINT":
                print(get_var(line[1], variables))
        program_counter += 1


def repl():
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


def main():
    if len(sys.argv) < 2:
        repl()
    else:
        interpret(open(sys.argv[1], "r").read())


if __name__ == "__main__":
    main()
