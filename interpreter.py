#!/usr/bin/python3
import sys

add = lambda x, y: int(x)+int(y)
sub = lambda x, y: int(x)-int(y)
mul = lambda x, y: int(x)*int(y)
div = lambda x, y: int(x)/int(y)

def handle_line(line, func):
    arr = []
    arr = line.split()
    print(func(arr[1], arr[2]))

def interpret(code):
    for line in code.splitlines():
        arr = []
        if line.startswith("ADD "):
            handle_line(line, add)
        elif line.startswith("SUB "):
            handle_line(line,sub)
        elif line.startswith("MUL "):
            handle_line(line, mul)
        elif line.startswith("DIV "):
            if line.split()[2] != "0":
                handle_line(line, div)
            else:
                print("div by zero")

def main():
    interpret(open(sys.argv[2], 'r').read())
