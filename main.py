#!/usr/bin/env python3
# coding: utf-8

import argparse
from typing import Dict, List, Union, Any, Optional

from lbuiltins import BUILTINS, Atom, Proc, LList


def listing(expr: str, parent: Union[None, LList] = None) -> Union[Atom, LList]:
    """from an expresion create a 1 dimension listing"""
    sub_expr = [""]  # type: List[str]
    i = 0
    depth = 0
    max_depth = 0
    for l in expr:
        if l == "(":
            depth += 1
            max_depth += 1
            if depth <= 1:
                continue
        elif l == ")":
            depth -= 1
            if depth <= 0:
                continue
        if (
            depth <= 0
            and l.isspace()
            and len(sub_expr) == i + 1
            and len(sub_expr[i]) > 0
        ):
            i += 1
            continue
        if len(sub_expr) <= i and not l.isspace():
            sub_expr.append(l)
        else:
            sub_expr[-1] += l

    if len(sub_expr) == 1 and max_depth == 0:
        return Atom(sub_expr[0].strip())

    current_list = LList()
    print(sub_expr)
    for e in sub_expr:
        current_list.childs.append(listing(f"{e}", current_list))
    return current_list


def execute_file(filename: str, state: Dict) -> int:
    with open(filename, "r") as script_file:
        script = script_file.read()
        e = listing(script, None)
        print(f"EXPR::{e}")
        e.evaluate(state)
        return 0


def main() -> int:
    state = {}  # type: Dict[str, str]

    # LOAD STD LSL (Loïc Standard Library)
    execute_file("std.lisp", state)

    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?", default="")
    args = parser.parse_args()
    if args.file:
        return execute_file(args.file, state)

    print("Welcome to Loïc Lisp interpreter (llisp)")
    print("Type exit to exit")
    while True:
        user_in = input(">>> ")
        if user_in == "exit":
            return 0
        else:
            e = listing(user_in, None)
            print(f"EXPR::{e}")
            evaluation = e.evaluate(state)
            if evaluation is not None:
                print(f"<<< {evaluation.value}")


if __name__ == "__main__":
    main()
