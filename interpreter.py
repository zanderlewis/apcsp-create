#!/usr/bin/python3
import sys
import math


def add(args, vars):
    return float(get_var(args[0], vars)) + float(get_var(args[1], vars))


def sub(args, vars):
    return float(get_var(args[0], vars)) - float(get_var(args[1], vars))


def mul(args, vars):
    return float(get_var(args[0], vars)) * float(get_var(args[1], vars))


def div(args, vars):
    return float(get_var(args[0], vars)) / float(get_var(args[1], vars))


def sine(args, vars):
    return math.sin(float(get_var(args[0], vars)))


def cosine(args, vars):
    return math.cos(float(get_var(args[0], vars)))


def tangent(args, vars):
    return math.tan(float(get_var(args[0], vars)))


OPERATION_MAP = {
    "+": (add, 2),
    "-": (sub, 2),
    "*": (mul, 2),
    "/": (div, 2),
    "sin": (sine, 1),
    "cos": (cosine, 1),
    "tan": (tangent, 1),
}


def handle_expr(line, variables):
    # First, we skip the first two elements if setting variables, first element if PRINT
    # ['let', 'a', '=', '0'] OR ['let', 'a', '=', '2', '+', '3'] OR ['print', 'a']
    line = line[2:] if line[0] == "let" else line[1:]
    # line[0] is `=` if it's a let statement
    if line[0] == "=":
        line = line[1:]  # Skip the '='
    # Now we have the actual expression, which can be a single value or an operation
    if len(line) == 1:
        return get_var(line[0], variables)
    else:
        # Math operation, we expect something like ['2', '+', '3'] or ['a', '*', 'b']
        left = line[0]
        op = line[1].lower()
        right = line[2]
        if op in OPERATION_MAP:
            func, arg_count = OPERATION_MAP[op]
            if arg_count == 2:
                return func([left, right], variables)
            elif arg_count == 1:
                return func([left], variables)
            else:
                raise ValueError(f"Unsupported number of arguments for operator {op}")
        else:
            raise ValueError(f"Unknown operator: {op}")


def get_var(keyword, variables):
    """
    This function retrieves variables if they exist,
    else they return the passed keyword back to the program.
    """
    if keyword in variables:
        return variables[keyword]
    return keyword


def handle_let(line, variables, program_counter):
    """This function handles variable assignment."""
    var_name = line[1]
    # Evaluate the expression on the right side of the '='
    expr_result = handle_expr(line, variables)
    variables[var_name] = expr_result
    return variables, program_counter + 1


def handle_ifgoto(line, variables, labels, program_counter):
    """This function handles ifgoto statements and adds a ton of comparison operators."""
    vval = float(get_var(line[1], variables))
    comp_val = float(get_var(line[3], variables))
    label = line[4]
    operator = line[2]
    condition_met = False

    match operator:
        case "==":
            condition_met = vval == comp_val
        case "!=":
            condition_met = vval != comp_val
        case "<":
            condition_met = vval < comp_val
        case "<=":
            condition_met = vval <= comp_val
        case ">":
            condition_met = vval > comp_val
        case ">=":
            condition_met = vval >= comp_val
        case _:
            raise ValueError(f"Unknown operator: {operator}")

    if condition_met:
        return labels[label]
    return program_counter + 1


def interpret(code):
    """This function interprets the language code and ultimately runs it."""
    lines = code.splitlines()
    variables = {}
    labels = {}  # Labels allow goto statements for loops.

    # First, we ignore comments, both in-line and full-line comments
    cleaned_lines = []
    for line in lines:
        line = line.split(";", 1)[0].strip()  # A nod towards BASIC/Assembly
        if line:  # Only add non-empty lines
            cleaned_lines.append(line)
    lines = cleaned_lines

    # Secondly, we collect labels
    for i, line in enumerate(lines):
        parts = line.split()
        if parts and parts[0].lower() == "label":
            labels[parts[1]] = i  # Add label and line number

    # Next, we run the interpreter like normal
    program_counter = 0
    while program_counter < len(lines):
        line = lines[program_counter].split()

        # Empty line
        if not line:
            program_counter += 1
            continue

        match line[0].lower():
            case "let":
                variables, program_counter = handle_let(
                    line, variables, program_counter
                )
                continue  # We already updated the program counter
            case "goto":
                program_counter = labels[line[1]]
                continue  # We want to jump straight to the LABEL location
            case "ifgoto":
                program_counter = handle_ifgoto(
                    line, variables, labels, program_counter
                )
                continue  # handle_ifgoto will update the program counter if needed
            case "print":
                print(float(handle_expr(line, variables)))
        program_counter += 1


def repl():
    print("Loading REPL...")
    print(
        "[WARNING] REPL does not support multi-line statements or labels. Use a file for more complex code."
    )
    print("Type 'exit' or 'quit' to exit.")
    try:
        while True:
            line = input(">>> ")
            if line.strip().lower() in ["exit", "quit"]:
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
