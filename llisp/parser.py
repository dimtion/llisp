from typing import List, Tuple, Union

from llisp.lbuiltins import Atom, LList, create_atom


def lexer(expr: str) -> Tuple[List[str], int]:
    sub_expr: List[str] = [""]
    i = 0
    depth = 0
    max_depth = 0
    expr = expr.strip()
    in_string = False
    for e in expr:
        if in_string:
            sub_expr[-1] += e
            if e in "'\"":
                in_string = False
            continue
        elif e == "(":
            depth += 1
            max_depth += 1
            if depth <= 1:
                continue
        elif e == ")":
            depth -= 1
            if depth <= 0:
                continue
        elif e in "'\"":
            in_string = True
        if (
            depth <= 0
            and e.isspace()
            and len(sub_expr) == i + 1
            and len(sub_expr[i]) > 0
        ):
            i += 1
            continue
        if len(sub_expr) <= i and not e.isspace():
            sub_expr.append(e)
        else:
            sub_expr[-1] += e

    return sub_expr, max_depth


def expand_str(expr: List[str], max_depth) -> Union[List[str], Atom]:
    """Create a list of char from the string notation or return an atom object"""
    if len(expr) == 1 and max_depth == 0:
        current_expr = expr[0].strip()
        if current_expr[0] == current_expr[-1] == '"':
            new_expr = "(list"
            for c in current_expr[1:-1]:
                c = f" '{c}'"
                new_expr += c
            new_expr += ")"
            expr[0] = new_expr

        else:
            return create_atom(expr[0].strip())

    return expr


def atomize(expr: List["str"]):
    """Instanciate Atoms and sub LList from the tokens"""
    current_list = LList()
    # print(expr)
    for e in expr:
        current_list.childs.append(listing(f"{e}", current_list))
    return current_list


def listing(expr: str, parent: Union[None, LList] = None) -> Union[Atom, LList]:
    """From an expression returns an AST tree that can be evaluated"""
    tokens, max_depth = lexer(expr)
    expanded_tokens = expand_str(tokens, max_depth)
    if isinstance(expanded_tokens, Atom):
        return expanded_tokens
    return atomize(tokens)
