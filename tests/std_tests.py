from typing import Dict, List

import pytest

from llisp.main import load_std
from llisp.parser import listing


@pytest.fixture
def std_state() -> Dict[str, object]:
    state: Dict[str, object] = {}
    load_std(state)
    return state


def simple_multi_std(
    std_state: Dict[str, object], test_inputs: List[str], expected: str
) -> None:
    state = std_state
    out = None
    for t in test_inputs:
        e = listing(t, None)
        out = e.evaluate(state).value

    assert str(out) == expected


@pytest.mark.parametrize(
    "test_inputs,expected",
    [
        (["(bool 1)"], "1"),
        (["(bool 0)"], "0"),
        (["(bool 5)"], "1"),
        (["(bool '1')"], "1"),
        (["(var a -5)", "(bool a)"], "1"),
    ],
)
def test_bool(
    std_state: Dict[str, object], test_inputs: List[str], expected: str
) -> None:
    return simple_multi_std(std_state, test_inputs, expected)


@pytest.mark.parametrize(
    "test_inputs,expected",
    [
        (["(! 1)"], "0"),
        (["(! 0)"], "1"),
        (["(! 5)"], "0"),
        (["(var a -5)", "(! a)"], "0"),
    ],
)
def test_not(
    std_state: Dict[str, object], test_inputs: List[str], expected: str
) -> None:
    return simple_multi_std(std_state, test_inputs, expected)


@pytest.mark.parametrize(
    "test_inputs,expected",
    [
        (["(and 1 1)"], "1"),
        (["(and 2 1)"], "1"),
        (["(and 0 1)"], "0"),
        (["(and 1 0)"], "0"),
        (["(and 0 0)"], "0"),
        (["(and 5 'a')"], "1"),
    ],
)
def test_and(
    std_state: Dict[str, object], test_inputs: List[str], expected: str
) -> None:
    return simple_multi_std(std_state, test_inputs, expected)


@pytest.mark.parametrize(
    "test_inputs,expected",
    [
        (["(or 0 0)"], "0"),
        (["(or 2 1)"], "1"),
        (["(or 0 1)"], "1"),
        (["(or 1 0)"], "1"),
        (["(or 5 'a')"], "1"),
    ],
)
def test_or(
    std_state: Dict[str, object], test_inputs: List[str], expected: str
) -> None:
    return simple_multi_std(std_state, test_inputs, expected)


@pytest.mark.parametrize(
    "test_inputs,expected",
    [
        (["(xor 0 0)"], "0"),
        (["(xor 2 1)"], "0"),
        (["(xor 0 1)"], "1"),
        (["(xor 1 0)"], "1"),
        (["(xor 5 'a')"], "0"),
        (["(xor 5 0)"], "1"),
    ],
)
def test_xor(
    std_state: Dict[str, object], test_inputs: List[str], expected: str
) -> None:
    return simple_multi_std(std_state, test_inputs, expected)


@pytest.mark.parametrize(
    "test_inputs,expected",
    [
        (["(min 0 0)"], "0"),
        (["(min 2 1)"], "1"),
        (["(min 0 1)"], "0"),
        (["(min 1 0)"], "0"),
        (["(min 5 0)"], "0"),
        (["(min 5 -10)"], "-10"),
    ],
)
def test_min(
    std_state: Dict[str, object], test_inputs: List[str], expected: str
) -> None:
    return simple_multi_std(std_state, test_inputs, expected)


@pytest.mark.parametrize(
    "test_inputs,expected",
    [
        (["(chartoint '0')"], "0"),
        (["(chartoint '1')"], "1"),
        (["(chartoint '2')"], "2"),
        (["(chartoint '3')"], "3"),
        (["(chartoint '9')"], "9"),
    ],
)
def test_chartoint(
    std_state: Dict[str, object], test_inputs: List[str], expected: str
) -> None:
    return simple_multi_std(std_state, test_inputs, expected)


@pytest.mark.parametrize(
    "test_inputs,expected",
    [
        (['(toint "0")'], "0"),
        (['(toint "1")'], "1"),
        (['(toint "11")'], "11"),
        (['(toint "123")'], "123"),
        (['(toint "9029")'], "9029"),
    ],
)
def test_toint(
    std_state: Dict[str, object], test_inputs: List[str], expected: str
) -> None:
    return simple_multi_std(std_state, test_inputs, expected)
