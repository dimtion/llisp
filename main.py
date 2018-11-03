#!/usr/bin/env python3
# coding: utf-8

from typing import Dict, List, Union, Any, Optional

from lbuiltins import BUILTINS, Atom, Proc, LList


def listing(expr: str, parent: Union[None, LList] = None) -> Union[Atom, LList]:
    """from an expresion create a 1 dimension listing"""
    sub_expr = []  # type: List[str]
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
            if depth <= 1:
                continue
        if depth <= 1 and l == " " and len(sub_expr) == i + 1:
            i += 1
            continue
        if len(sub_expr) <= i:
            sub_expr.append(l)
        else:
            sub_expr[i] += l

    if len(sub_expr) == 1 and max_depth == 0:
        return Atom(sub_expr[0])

    current_list = LList()
    for e in sub_expr:
        current_list.childs.append(listing(f"{e}", current_list))
    return current_list


def main() -> int:
    print("Welcome to Loïc Lisp interpreter (llisp)")
    print("Type exit to exit")
    state = {}  # type: Dict[str, str]
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
