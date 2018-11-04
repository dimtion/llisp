Loïc Lisp Interpreter (Llisp)
=============================

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
        
A simple Lisp interpreter for educational purposes

## Installation and usage

Clone the repository and install:
```bash
git clone git@github.com:dimtion/llisp.git
cd llisp
pip install .
```

You can launch a REPL with the following command line:
```
$ lisplang
Welcome to Loïc Lisp interpreter (llisp)
Type exit to exit
>>>
```

## Some examples commands:

Prompt a variable:
```
>>> 5
<<< 5

>>> (+ 2 3)
<<< 5
```

Variable declaration and assignation:
```
>>> (var n 10)
<<< n
>>> (* 5 n)
<<< 50
```

Function declaration and function call:
```
>>> (def (sum x y) (+ x y))
<<< sum
>>> (sum 33 17)
<<< 50
```

## Features

Those are the features that are currently implemented, more to come in the
future:

* REPL and file source code input
* Arithmetic operators (int, floats)
* Variable declaration and assignation
* Conditionals if
* Function declaration and call
* Recursive functions
* List manipulation
* String creation and  manipulation
* Simple standard library
