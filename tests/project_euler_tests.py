from typing import Dict, Union

import pytest

from llisp.lbuiltins import Atom, LList
from llisp.main import execute_file, load_std
from tests.std_tests import std_state  # noqa: F401


def simple_test_file(  # noqa: F811
    std_state: Dict[str, Union[LList, Atom]], test_file: str, expected: str
) -> None:
    state = std_state
    load_std(state)
    execute_file(test_file, state)

    assert state["output"].value == expected


@pytest.mark.parametrize(  # noqa: F811
    "test_file,expected",
    [
        ("project_euler/problem1.lisp", 233_168),
        ("project_euler/problem2.lisp", 4_613_732),
    ],
)
def test_problem(std_state: Dict[str, object], test_file: str, expected: str) -> None:
    return simple_test_file(std_state, test_file, expected)
