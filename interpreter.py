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

def handle_line(line, func):
    print(func(line))

def interpret(code):
    lines = 0
    for line in code.splitlines():
        lines += 1
        line = line.split()
        match line[0]:
            case "ADD": handle_line(line, add)
            case "SUB": handle_line(line, sub)
            case "MUL": handle_line(line, mul)
            case "DIV":
                if line[2] == "0":
                    print(f"error: div by zero on line {lines}")
                else:
                    handle_line(line, div)
            case "SIN": handle_line(line, sine)
            case "COS": handle_line(line, cosine)
            case "TAN": handle_line(line, tangent)

def main():
    if len(sys.argv) < 2:
        print("Loading REPL...")
        print("Type 'exit' to exit.")
        while True:
            line = input(">>> ")
            if line == "exit":
                break
            interpret(line)
    else:
        interpret(open(sys.argv[1], 'r').read())

if __name__ == "__main__":
    main()
