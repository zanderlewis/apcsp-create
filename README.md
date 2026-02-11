# apcsp-create
This programming language is designed to be a very small, but Turing complete language. This was created as my AP Computer Science Principles Create Performance Task for my AP Exam.

## Syntax
The syntax of this language is very simple. Each line is a statement, and statements are separated by newlines. The language supports the following statements:

* `let key = value` - This statement assigns a value to a variable. The value can be a number, an expression, or another variable.
* `print value` - This statement prints a number, an expression, or a variable to the console.
* `label key` - This statement defines a label that can be jumped to using the `if` statement.
* `goto label` - This statement jumps to a label defined by the `label` statement.
* `if value1 operator value2 goto label` - This statement compares two values using an operator and jumps to a label if the condition is met. The supported operators are `==`, `!=`, `<`, `>`, `<=`, and `>=`.
* `; comment` - This statement is a comment and is ignored by the interpreter, both inline and full-line.

## Example
Here is an example of a program written in this language that calculates the factorial of a number:
```
; Initialize parameters
let f = 1
let i = 0
let n = 52  ; Change this variable

label mult
let i = i + 1
let f = f * i
if i != n goto mult
print f
```

And the fibonacci sequence:
```
; Initialize parameters
let a = 0
let b = 1
let n = 10  ; Change this variable

label loop
print a  ; Print current fibonacci number

; Fibonacci magic
let temp = a + b
let a = b
let b = temp
let n = n - 1

; Break out of the loop if n is 0, else keep looping
if n == 0 goto end
goto loop

label end  ; All done
```

## Running the Interpreter
To run the interpreter, you will need to have Python installed on your computer. You can then run the interpreter by executing one of the following commands in your terminal:
```
python interpreter.py path/to/your/program.math
python3 interpreter.py path/to/your/program.math
uv run interpreter.py path/to/your/program.math
```

## Gotchas
* The `if` statement must have the format `if value1 operator value2 goto label`. If the `goto` keyword is missing or in the wrong place, the interpreter will raise an error.
* Variables are case-sensitive, so `let x = 5` and `let X = 5` are two different variables.
* Expressions are very simple, so you can only run one expression per line. For example, `let x = 5 + 3` is valid, but `let x = 5 + 3 * 2` is not. You would need to break it up into multiple lines:
```
let temp = 3 * 2
let temp = temp + 5
```
