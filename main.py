#!/usr/bin/env python3
# coding: utf-8

from typing import Dict, List, Union, Any, Optional
from enum import Enum


class Atom(object):
    class AtomTypes(Enum):
        NUM = 1
        STR = 2
        NAME = 3
        VAR = 4
        PROC = 5

    def __init__(self, value: str):
        self.value_str = value
        self.parse()

    def parse(self):
        if is_int(self.value_str):
            self.value = int(self.value_str)
            self.type = self.AtomTypes.NUM
        elif is_name(self.value_str):
            self.value = self.value_str
            self.type = self.AtomTypes.NAME

    def evaluate(self, state: Dict) -> "Atom":
        if self.type == self.AtomTypes.NAME:
            return state[self.value].evaluate(state)
        return self

    # For num
    def plus(self, other: "Atom"):
        return Atom(self.value + other.value)

    def minus(self, other: "Atom"):
        return Atom(self.value - other.value)

    def times(self, other: "Atom"):
        return Atom(self.value * other.value)

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __repr__(self):
        return f"({self.type}) {self.value}"


class Proc(Atom):
    def __init__(self, name: "Atom", params: "LList", body: "Union[Atom, LList]"):
        self.name = name
        self.params = params
        self.body = body
        self.value = name
        self.type = self.AtomTypes.PROC

    def evaluate_proc(self, state: Dict, sub_state: Dict) -> Atom:
        temp_state = {**state, **sub_state}
        return self.body.evaluate(temp_state)


def is_int(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_name(s: str) -> bool:
    """returns if the token is a valid variable name"""
    if len(s) <= 0:
        return False
    if is_int(s[0]):
        return False

    if s in s in "*+-/":
        return True
    return s.isalnum()


class LList(object):
    def __init__(self):
        self.childs = []  # type: List[Union[LList, Atom]]

    def evaluate(self, state: Union[Dict]) -> Atom:
        action = self.childs[0]
        if not isinstance(action, Atom):
            raise Exception(f"ERR: {action} not atomic")
        if action.type == Atom.AtomTypes.NUM:
            return action
        if action.value_str == "+":
            x = self.childs[1].evaluate(state)
            for y in self.childs[2:]:
                x = x.plus(y.evaluate(state))
            return x
        if action.value_str == "-":
            x = self.childs[1].evaluate(state)
            for y in self.childs[2:]:
                x = x.minus(y.evaluate(state))
            return x

        if action.value_str == "*":
            x = self.childs[1].evaluate(state)
            for y in self.childs[2:]:
                x = x.times(y.evaluate(state))
            return x

        if action.value_str == "if":
            req = self.childs[1].evaluate(state)
            if req.value != 0:
                return self.childs[2].evaluate(state)
            else:
                return self.childs[3].evaluate(state)

        if action.value_str == "eq":
            left = self.childs[1].evaluate(state)
            right = self.childs[2].evaluate(state)
            if left == right:
                return Atom("1")
            else:
                return Atom("0")

        if (
            action.value_str == "var"
            and isinstance(self.childs[1], Atom)
            and self.childs[1].type == Atom.AtomTypes.NAME
        ):
            state[self.childs[1].value] = self.childs[2].evaluate(state)
            print(f"<<< {self.childs[1].value} = {self.childs[2]}")
            return self.childs[1]

        if action.value_str == "def" and isinstance(self.childs[1], LList):
            name = self.childs[1].childs[0]
            params = LList()
            params.childs = self.childs[1].childs[1:]
            body = self.childs[2]

            a = Proc(name, params, body)
            state[self.childs[1].childs[0].value] = a
            print(f"<<< ({a} {a.params})")
            return self.childs[1].childs[0]
        elif action.value_str in state:
            proc = state[action.value_str]
            if proc.type == Atom.AtomTypes.PROC:
                sub_state = {}  # type: Dict[str, Union[LList, Atom]]
                for p, c in zip(proc.params.childs, self.childs[1:]):
                    sub_state[p.value_str] = c.evaluate(state)
                # print(f"Evaluating {proc} with {state} and {sub_state}")
                return proc.evaluate_proc(state, sub_state)

        print(state)
        raise Exception(f"ERR: Symbol {action} unknown")

    def __repr__(self):
        return str(self.childs)


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
