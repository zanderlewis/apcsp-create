#!/usr/bin/python3
import math
import shlex
import sys


def is_str_literal(s):
    return isinstance(s, str) and s.startswith('"') and s.endswith('"')


def check_str(args, left, right):
    arg0_is_str = is_str_literal(args[0]) if len(args) > 0 else False
    arg1_is_str = is_str_literal(args[1]) if len(args) > 1 else False
    if arg0_is_str or arg1_is_str or isinstance(left, str) or isinstance(right, str):
        return True
    return False


def add(args, vars):
    left = get_var(args[0], vars)
    right = get_var(args[1], vars)
    if check_str(args, left, right):
        return str(left) + str(right)
    return float(left) + float(right)


def sub(args, vars):
    left = get_var(args[0], vars)
    right = get_var(args[1], vars)
    if check_str(args, left, right):
        raise ValueError("Subtraction is not supported for strings")
    return float(left) - float(right)


def mul(args, vars):
    left = get_var(args[0], vars)
    right = get_var(args[1], vars)
    if check_str(args, left, right):
        raise ValueError("Multiplication is not supported for strings")
    return float(left) * float(right)


def div(args, vars):
    left = get_var(args[0], vars)
    right = get_var(args[1], vars)
    if check_str(args, left, right):
        raise ValueError("Division is not supported for strings")
    return float(left) / float(right)


def mod(args, vars):
    left = get_var(args[0], vars)
    right = get_var(args[1], vars)
    if check_str(args, left, right):
        raise ValueError("Modulus is not supported for strings")
    return float(left) % float(right)


def power(args, vars):
    left = get_var(args[0], vars)
    right = get_var(args[1], vars)
    if check_str(args, left, right):
        raise ValueError("Exponentiation is not supported for strings")
    return float(left) ** float(right)


def sine(args, vars):
    left = get_var(args[0], vars)
    if check_str(args, left, None):
        raise ValueError("Sine is not supported for strings")
    return math.sin(float(left))


def cosine(args, vars):
    left = get_var(args[0], vars)
    if check_str(args, left, None):
        raise ValueError("Cosine is not supported for strings")
    return math.cos(float(left))


def tangent(args, vars):
    left = get_var(args[0], vars)
    if check_str(args, left, None):
        raise ValueError("Tangent is not supported for strings")
    return math.tan(float(left))


def square_root(args, vars):
    left = get_var(args[0], vars)
    if check_str(args, left, None):
        raise ValueError("Square root is not supported for strings")
    return math.sqrt(float(left))


OPERATION_MAP = {
    "+": (add, 2),
    "-": (sub, 2),
    "*": (mul, 2),
    "/": (div, 2),
    "%": (mod, 2),
    "^": (power, 2),
    "sin": (sine, 1),
    "cos": (cosine, 1),
    "tan": (tangent, 1),
    "sqrt": (square_root, 1),
}


def handle_expr(line, variables):
    line = line[2:] if line[0] == "let" else line[1:]
    if line[0] == "=":
        line = line[1:]
    if len(line) == 1:
        return get_var(line[0], variables)
    elif len(line) == 2:
        # Single-argument operation, e.g., ['sqrt', 'num']
        op = line[0].lower()
        arg = line[1]
        if op in OPERATION_MAP:
            func, arg_count = OPERATION_MAP[op]
            if arg_count == 1:
                return func([arg], variables)
            else:
                raise ValueError(f"Unsupported number of arguments for operator {op}")
        else:
            raise ValueError(f"Unknown operator: {op}")
    else:
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
    if is_str_literal(keyword):
        return keyword[1:-1]
    try:
        return float(keyword)
    except ValueError:
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
    if line[4].lower() != "goto":
        raise ValueError("Expected 'goto' in if statement")
    label = line[5]  # line[4] is "goto", line[5] is the label name
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
        parts = shlex.split(line)
        if parts and parts[0].lower() == "label":
            labels[parts[1]] = i  # Add label and line number

    # Next, we run the interpreter like normal
    program_counter = 0
    while program_counter < len(lines):
        line = shlex.split(lines[program_counter])

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
            case "if":
                program_counter = handle_ifgoto(
                    line, variables, labels, program_counter
                )
                continue  # handle_ifgoto will update the program counter if needed
            case "print":
                result = handle_expr(line, variables)
                if isinstance(result, (int, float)):
                    print(float(result))
                else:
                    print(result)
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
