import copy
from enum import Enum
from typing import Any, Callable, Dict, List, Union


class ParseError(Exception):
    pass


class UndefinedError(Exception):
    pass


class NotCallable(Exception):
    pass


class Atom(object):
    class AtomTypes(Enum):
        NUM = 1
        CHAR = 2
        NAME = 3
        VAR = 4
        PROC = 5
        LIST = 6

    value: Any = None

    def __init__(self, value: Union[str, "LList"]):
        if isinstance(value, str):
            self.value_str = value.strip()
            self.parse()
        else:
            self.value_str = str(value)
            self.value = value
            self.type = self.AtomTypes.LIST

    def parse(self):
        if is_int(self.value_str):
            self.value = int(self.value_str)
            self.type = self.AtomTypes.NUM
        elif is_float(self.value_str):
            self.value = float(self.value_str)
            self.type = self.AtomTypes.NUM
        elif is_char(self.value_str):
            iner_char = bytes(self.value_str[1:-1], "utf-8").decode("unicode_escape")
            if len(iner_char) > 1:
                raise ParseError(f"Parse ERROR: {self.value_str} is not a CHAR")
            self.value = iner_char
            self.type = self.AtomTypes.CHAR
        elif is_name(self.value_str):
            self.value = self.value_str
            self.type = self.AtomTypes.NAME
        else:
            raise ParseError(f"Parse ERROR: {self.value_str}")

    def evaluate(self, state: Dict) -> "Atom":
        if self.type in [self.AtomTypes.LIST, self.AtomTypes.NUM, self.AtomTypes.CHAR]:
            return self

        raise Exception(f"Cannot evaluate {self}")

    # For NUM type
    def plus(self, other: "Atom"):
        return Atom(str(self.value + other.value))

    def minus(self, other: "Atom"):
        return Atom(str(self.value - other.value))

    def times(self, other: "Atom"):
        return Atom(str(self.value * other.value))

    def divide(self, other: "Atom"):
        return Atom(str(self.value / other.value))

    def divide_int(self, other: "Atom"):
        return Atom(str(self.value // other.value))

    # Primitives for every Atom
    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __lt__(self, other):
        return self.type == other.type and self.value < other.value

    def modulo(self, other):
        return Atom(str(self.value % other.value))

    def __repr__(self):
        return f"({self.type}) {self.value}"


class Name(Atom):
    def __init__(
        self,
        name: str,
        body: Union[Atom, "LList", None] = None,
        params: Union["LList", None] = None,
    ):
        self.name = name
        self.params = params
        self.value = body
        self.value_str = name
        self.type = self.AtomTypes.NAME

    def evaluate(self, state: Dict) -> Atom:
        """
        Name evaluation that makes the correspondance between the Name and
        the corresponding Atom
        """
        if self.value in state:
            return state[self.name].evaluate(state)
        raise UndefinedError(f"{self.name} Undefined")

    def call_proc(self, state: Dict, sub_state: Dict) -> Atom:
        temp_state = {**state, **sub_state}
        if isinstance(self.value, LList):
            for child in self.value.childs[2:]:
                result = child.evaluate(temp_state)
        return result


def create_atom(value: str) -> Union["Atom", "Name"]:
    atom = Atom(value)
    if is_int(value):
        atom.value = int(value)
        atom.type = atom.AtomTypes.NUM
    elif is_float(value):
        atom.value = float(value)
        atom.type = atom.AtomTypes.NUM
    elif is_char(value):
        iner_char = bytes(value[1:-1], "utf-8").decode("unicode_escape")
        if len(iner_char) > 1:
            raise ParseError(f"Parse ERROR: {value} is not a CHAR")
        atom.value = iner_char
        atom.type = atom.AtomTypes.CHAR
    elif is_name(value):
        atom = Name(value)
        atom.value = atom.value_str
        atom.type = atom.AtomTypes.NAME
    return atom


# Parsing functions


def is_int(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_char(s: str) -> bool:
    return s[0] == s[-1] == "'"


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
        if not l.isalnum() and l not in "*+-/<>=!@#$%^&[]":
            return False
    return True


class Expression(object):
    pass


class Program(object):
    pass


class LList(object):
    def __init__(self):
        self.childs: List[Union[LList, Atom]] = []

    def evaluate(self, state: Union[Dict]) -> Atom:
        action = self.childs[0]
        if isinstance(action, LList):
            # If the childs are LList that means that we want to execute them
            # linearly. We return the result of the last child.
            # TODO: This should move into a `Program`, but what about a
            # function which is also a list of LList
            for child in self.childs:
                result = child.evaluate(state)
            return result
        if action.type == Atom.AtomTypes.NAME:
            if action.value_str in BUILTINS:
                return BUILTINS[action.value_str](self, state)
            elif action.value_str in state:
                return custom_op(action.value_str, self, state)

        raise UndefinedError(f"ERR: Symbol {action} unknown")

    def __eq__(self, other):
        if len(self.childs) != len(other.childs):
            return False
        for s, o in zip(self.childs, other.childs):
            if s != o:
                return False
        return True

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


def divide_int_op(expr: "LList", state: Dict) -> "Atom":
    x = expr.childs[1].evaluate(state)
    for y in expr.childs[2:]:
        x = x.divide_int(y.evaluate(state))
    return x


def mod_op(expr: "LList", state: Dict) -> "Atom":
    x = expr.childs[1].evaluate(state)
    y = expr.childs[2].evaluate(state)
    return x.modulo(y)


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
    if isinstance(left, Atom) and left < right:
        return Atom("1")
    else:
        return Atom("0")


def var_op(expr: "LList", state: Dict) -> "Atom":
    if (
        len(expr.childs) == 3
        and isinstance(expr.childs[1], Atom)
        and expr.childs[1].type == Atom.AtomTypes.NAME
    ):
        state[expr.childs[1].value] = expr.childs[2].evaluate(state)
        # print(f"<<< {expr.childs[1].value} = {expr.childs[2]}")
        return expr.childs[1]
    else:
        raise ParseError("Parse error: Unexpected format")


def def_op(expr: "LList", state: Dict) -> Atom:
    if isinstance(expr.childs[1], LList):
        name = expr.childs[1].childs[0]
        params = LList()
        params.childs = expr.childs[1].childs[1:]
        body = expr

        if not isinstance(name, Atom):
            raise ParseError(f"Parse error: Unexpected format of function name f{name}")

        a = Name(name.value, body, params)
        state[name.value] = a
        # print(f"<<< ({a} {a.params})")
        return name
    raise ParseError("Parse error: Unexpected format")


def custom_op(name: str, expr: "LList", state: Dict) -> "Atom":
    proc = state[name]
    if proc.type == Atom.AtomTypes.NAME:
        sub_state: Dict[str, Union[LList, Atom]] = {}
        for p, c in zip(proc.params.childs, expr.childs[1:]):
            sub_state[p.value_str] = c.evaluate(state)
        # print(f"Evaluating {proc} with {state} and {sub_state}")
        return proc.call_proc(state, sub_state)
    raise NotCallable(f"{name} not a procedure")


def echo_op(expr: "LList", state: Dict) -> "Atom":
    e = expr.childs[1].evaluate(state)
    print(e.value, end="", flush=True)
    return e


def print_op(expr: "LList", state: Dict) -> "Atom":
    e = expr.childs[1].evaluate(state)
    print(e.value_str)
    return e


def list_op(expr: "LList", state: Dict) -> "Atom":
    new_list = LList()
    if len(expr.childs) > 1:
        for c in expr.childs[1:]:
            new_list.childs.append(copy.deepcopy(c).evaluate(state))
    return Atom(new_list)


def push_op(expr: "LList", state: Dict) -> "Atom":
    e = expr.childs[1].evaluate(state)
    old_list = expr.childs[2].evaluate(state)
    new_list = LList()
    new_list.childs.append(copy.deepcopy(e))
    if isinstance(old_list, Atom) and old_list.type == old_list.AtomTypes.LIST:
        for c in old_list.value.childs:
            new_list.childs.append(copy.deepcopy(c))
    else:
        raise Exception("Cannot push: not a list")

    return Atom(new_list)


def pop_op(expr: "LList", state: Dict) -> "Atom":
    old_list = expr.childs[1].evaluate(state)
    new_list = LList()
    if isinstance(old_list, Atom) and old_list.type == old_list.AtomTypes.LIST:
        for c in old_list.value.childs[1:]:
            new_list.childs.append(copy.deepcopy(c))

    return Atom(new_list)


def el_op(expr: "LList", state: Dict) -> "Atom":
    return expr.childs[1].evaluate(state).value.childs[0].evaluate(state)


BUILTINS: Dict[str, Callable[[LList, Dict], Atom]] = {
    "+": plus_op,
    "-": minus_op,
    "*": times_op,
    "/": divide_op,
    "//": divide_int_op,
    "%": mod_op,
    "if": if_op,
    "eq": eq_op,
    "<": less_op,
    "var": var_op,
    "def": def_op,
    "echo": echo_op,
    "print": print_op,
    "list": list_op,
    "push": push_op,
    "pop": pop_op,
    "el": el_op,
}
