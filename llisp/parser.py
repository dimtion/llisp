from typing import List, Union

from llisp.lbuiltins import Atom, LList


def listing(expr: str, parent: Union[None, LList] = None) -> Union[Atom, LList]:
    """from an expresion create a 1 dimension listing"""
    sub_expr: List[str] = [""]
    i = 0
    depth = 0
    max_depth = 0
    expr = expr.strip()
    for e in expr:
        if e == "(":
            depth += 1
            max_depth += 1
            if depth <= 1:
                continue
        elif e == ")":
            depth -= 1
            if depth <= 0:
                continue
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

    if len(sub_expr) == 1 and max_depth == 0:
        return Atom(sub_expr[0].strip())

    current_list = LList()
    # print(sub_expr)
    for e in sub_expr:
        current_list.childs.append(listing(f"{e}", current_list))
    return current_list
