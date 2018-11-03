from typing import Dict, Union, List
from enum import Enum


class Atom(object):
    class AtomTypes(Enum):
        NUM = 1
        CHAR = 2
        NAME = 3
        VAR = 4
        PROC = 5

    def __init__(self, value: str):
        self.value_str = value.strip()
        self.parse()

    def parse(self):
        if is_int(self.value_str):
            self.value = int(self.value_str)
            self.type = self.AtomTypes.NUM
        elif is_float(self.value_str):
            self.value = float(self.value_str)
            self.type = self.AtomTypes.NUM
        elif is_char(self.value_str):
            self.value = self.value_str[1]
            self.type = self.AtomTypes.CHAR
        elif is_name(self.value_str):
            self.value = self.value_str
            self.type = self.AtomTypes.NAME
        else:
            raise Exception(f"Parse ERROR: {self.value_str}")

    def evaluate(self, state: Dict) -> "Atom":
        if self.type == self.AtomTypes.NAME:
            return state[self.value].evaluate(state)
        return self

    # For num
    def plus(self, other: "Atom"):
        return Atom(str(self.value + other.value))

    def minus(self, other: "Atom"):
        return Atom(str(self.value - other.value))

    def times(self, other: "Atom"):
        return Atom(str(self.value * other.value))

    def divide(self, other: "Atom"):
        return Atom(str(self.value / other.value))

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __lt__(self, other):
        return self.type == other.type and self.value < other.value

    def __repr__(self):
        return f"({self.type}) {self.value}"


def is_int(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_char(s: str) -> bool:
    return len(s) == 3 and s[0] == s[2] == "'"


def is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_name(s: str) -> bool:
    """returns if the token is a valid variable name"""
    if len(s) <= 0:
        return False
    if is_int(s[0]):
        return False

    for l in s:
        if not l.isalnum() and l not in "*+-/<>=!@#$%^&":
            return False
    return True


class Proc(Atom):
    def __init__(self, name: "Atom", params: "LList", body: "LList"):
        self.name = name
        self.params = params
        self.body = body
        self.value = name
        self.type = self.AtomTypes.PROC

    def evaluate_proc(self, state: Dict, sub_state: Dict) -> Atom:
        temp_state = {**state, **sub_state}
        for child in self.body.childs[2:]:
            result = child.evaluate(temp_state)
        return result


class LList(object):
    def __init__(self):
        self.childs = []  # type: List[Union[LList, Atom]]

    def evaluate(self, state: Union[Dict]) -> Atom:
        action = self.childs[0]
        if not isinstance(action, Atom):
            for child in self.childs:
                result = child.evaluate(state)
            return result
        if action.type == Atom.AtomTypes.NUM:
            return action
        if action.type == Atom.AtomTypes.NAME:
            if action.value_str in BUILTINS:
                return BUILTINS[action.value_str](self, state)
            elif action.value_str in state:
                return custom_op(action.value_str, self, state)

        raise Exception(f"ERR: Symbol {action} unknown")

    def __repr__(self):
        return str(self.childs)


def plus_op(expr: "LList", state: Dict) -> "Atom":
    x = expr.childs[1].evaluate(state)
    for y in expr.childs[2:]:
        x = x.plus(y.evaluate(state))
    return x


def minus_op(expr: "LList", state: Dict) -> "Atom":
    x = expr.childs[1].evaluate(state)
    for y in expr.childs[2:]:
        x = x.minus(y.evaluate(state))
    return x


def times_op(expr: "LList", state: Dict) -> "Atom":
    x = expr.childs[1].evaluate(state)
    for y in expr.childs[2:]:
        x = x.times(y.evaluate(state))
    return x


def divide_op(expr: "LList", state: Dict) -> "Atom":
    x = expr.childs[1].evaluate(state)
    for y in expr.childs[2:]:
        x = x.divide(y.evaluate(state))
    return x


def if_op(expr: "LList", state: Dict) -> "Atom":
    req = expr.childs[1].evaluate(state)
    if req.value != 0:
        return expr.childs[2].evaluate(state)
    else:
        return expr.childs[3].evaluate(state)


def eq_op(expr: "LList", state: Dict) -> "Atom":
    left = expr.childs[1].evaluate(state)
    right = expr.childs[2].evaluate(state)
    if left == right:
        return Atom("1")
    else:
        return Atom("0")


def not_op(expr: "LList", state: Dict) -> "Atom":
    left = expr.childs[1].evaluate(state)
    if left.value == 0:
        return Atom("1")
    else:
        return Atom("0")


def less_op(expr: "LList", state: Dict) -> "Atom":
    left = expr.childs[1].evaluate(state)
    right = expr.childs[2].evaluate(state)
    if left < right:
        return Atom("1")
    else:
        return Atom("0")


def var_op(expr: "LList", state: Dict) -> "Atom":
    if isinstance(expr.childs[1], Atom) and expr.childs[1].type == Atom.AtomTypes.NAME:
        state[expr.childs[1].value] = expr.childs[2].evaluate(state)
        # print(f"<<< {expr.childs[1].value} = {expr.childs[2]}")
        return expr.childs[1]
    else:
        raise Exception("Unexpected format")


def def_op(expr: "LList", state: Dict) -> "Atom":
    if isinstance(expr.childs[1], LList):
        name = expr.childs[1].childs[0]
        params = LList()
        params.childs = expr.childs[1].childs[1:]
        body = expr

        if not isinstance(name, Atom):
            raise Exception(f"Unexpected format of function name f{name}")

        a = Proc(name, params, body)
        state[name.value] = a
        # print(f"<<< ({a} {a.params})")
        return name
    raise Exception("Unexpected format")


def custom_op(name: str, expr: "LList", state: Dict):
    proc = state[name]
    if proc.type == Atom.AtomTypes.PROC:
        sub_state = {}  # type: Dict[str, Union[LList, Atom]]
        for p, c in zip(proc.params.childs, expr.childs[1:]):
            sub_state[p.value_str] = c.evaluate(state)
        # print(f"Evaluating {proc} with {state} and {sub_state}")
        return proc.evaluate_proc(state, sub_state)


def echo_op(expr: "LList", state: Dict) -> "Atom":
    e = expr.childs[1].evaluate(state)
    print(e.value_str)
    return e


BUILTINS = {
    "+": plus_op,
    "-": minus_op,
    "*": times_op,
    "/": divide_op,
    "if": if_op,
    "eq": eq_op,
    # "!": not_op,
    "<": less_op,
    "var": var_op,
    "def": def_op,
    "echo": echo_op,
}
