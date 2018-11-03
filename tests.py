import pytest
from typing import Dict, List
from main import listing
from lbuiltins import is_int


def simple_multi(test_inputs: List[str], expected: str) -> None:
    state = {}  # type: Dict[str, object]
    out = None
    for t in test_inputs:
        e = listing(t, None)
        out = e.evaluate(state).value

    assert str(out) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("1", True),
        ("2", True),
        ("d", False),
        ("0", True),
        ("%", False),
        ("123%", False),
        ("a123%", False),
        ("aleber %", False),
    ],
)
def test_is_int(test_input: str, expected: bool) -> None:
    is_int(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("1", "1"),
        ("(+ 1 1)", "2"),
        ("(+ 2 1)", "3"),
        ("(+ (+ 5 2) 1)", "8"),
        ("(+ (+ 5 2) (+ 3 9)", "19"),
        ("(+ (+ 5 (+ 2 2) (+ 3 9)", "21"),
        ("(+ 1 -1)", "0"),
        ("(+ 1 1 1)", "3"),
    ],
)
def test_compute_plus(test_input: str, expected: str) -> None:
    e = listing(test_input, None)
    assert str(e.evaluate({}).value) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("1 ", "1"),
        (" 1", "1"),
        ("( 1)", "1"),
        ("(1 )", "1"),
        ("( + 1 1)", "2"),
        ("(+  1 1)", "2"),
        ("( +  1 1)", "2"),
        ("( + 1 (+ 1 1) )", "3"),
    ],
)
def test_input_variants(test_input: str, expected: str) -> None:
    e = listing(test_input, None)
    print(f"EXPR::{e}")
    assert str(e.evaluate({}).value) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("(- 1 1)", "0"),
        ("(- 2 1)", "1"),
        ("(- (- 5 2) 1)", "2"),
        ("(- 103 1 1 1)", "100"),
    ],
)
def test_compute_minus(test_input: str, expected: str) -> None:
    e = listing(test_input, None)
    assert str(e.evaluate({}).value) == expected


@pytest.mark.parametrize(
    "test_inputs,expected",
    [
        (["(var x 1)", "x"], "1"),
        (["(var y 100)", "y"], "100"),
        (["(var y 100)", "(var x 10)", "(+ x y)"], "110"),
    ],
)
def test_compute_var(test_inputs: List[str], expected: str) -> None:
    return simple_multi(test_inputs, expected)


@pytest.mark.parametrize(
    "test_inputs,expected",
    [
        (["(def (square x) (* x x))", "(square 5)"], "25"),
        (["(def (sum x y) (+ x y))", "(sum 100 20)"], "120"),
        (["(def (const x) 5)", "(const 3249)"], "5"),
        (
            [
                "(def (square x) (* x x))",
                "(def (sum x y) (+ x y))",
                "(def (hyp a b) (sum (square a) (square b)))",
                "(hyp 2 3)",
            ],
            "13",
        ),
    ],
)
def test_compute_def(test_inputs: List[str], expected: str) -> None:
    return simple_multi(test_inputs, expected)


@pytest.mark.parametrize(
    "test_inputs,expected",
    [
        (["(eq 1 1)"], "1"),
        (["(eq 1 2)"], "0"),
        (["(eq 2 (+ 1 1))"], "1"),
        (["(var x 5)", "(eq 5 x)"], "1"),
        (["(def (mul x y) (* x y))", "(eq 6 (mul 2 3))"], "1"),
        (["(def (mul x y) (* x y))", "(eq 6 (mul 3 3))"], "0"),
    ],
)
def test_compute_eq(test_inputs: List[str], expected: str) -> None:
    return simple_multi(test_inputs, expected)


@pytest.mark.parametrize(
    "test_inputs,expected",
    [(["(<= 1 1)"], "1"), (["(<= 2 1)"], "0"), (["(<= 1 2)"], "1")],
)
def test_compute_le(test_inputs: List[str], expected: str) -> None:
    return simple_multi(test_inputs, expected)


@pytest.mark.parametrize(
    "test_inputs,expected",
    [
        (["(if 1 1 0)"], "1"),
        (["(if 0 1 0)"], "0"),
        (["(if (eq 100 200) 1 0)"], "0"),
        (["(if (eq 100 100) 1 0)"], "1"),
        (["(if 1 (+ 100 200) 0)"], "300"),
        (["(var x 100)", "(var y 200)", "(if (eq x y) 1 0)"], "0"),
        (["(var x 100)", "(var y 100)", "(if (eq x y) 1 0)"], "1"),
        (["(var x 100)", "(var y 200)", "(if (eq x y) x y)"], "200"),
        (["(var x 100)", "(var y x)", "(if (eq x y) x 200)"], "100"),
    ],
)
def test_compute_if(test_inputs: List[str], expected: str) -> None:
    return simple_multi(test_inputs, expected)


@pytest.mark.parametrize(
    "test_inputs,expected",
    [
        (
            [
                "(def (isincr x y) (eq y (+ x 1)))",
                "(var a 2)",
                "(if (isincr 2 3) 10 0)",
            ],
            "10",
        ),
        (["(def (eqbis x y) (if (eq x y) 1 0)", "(eqbis 72 72)"], "1"),
        (["(def (eqbis x y) (if (eq x y) 1 0)", "(eqbis 72 79)"], "0"),
        (
            [
                "(def (eqbis x y) (if (eq x y) 1 0)",
                "(var x 10)",
                "(var b 100)",
                "(eqbis x b)",
            ],
            "0",
        ),
        (
            [
                "(def (eqbis x y) (if (eq x y) 1 0)",
                "(var x 10)",
                "(var b 10)",
                "(eqbis x b)",
            ],
            "1",
        ),
        (
            [
                "(def (eqbis x y) (if (eq x y) 1 0)",
                "(var x 10)",
                "(var b x)",
                "(eqbis x b)",
            ],
            "1",
        ),
        (
            ["(def (sumint x) (if (eq x 0) 0 (+ (sumint (- x 1)) x)))", "(sumint 0)"],
            "0",
        ),
        (
            ["(def (sumint x) (if (eq x 0) 0 (+ (sumint (- x 1)) x)))", "(sumint 1)"],
            "1",
        ),
        (
            ["(def (sumint x) (if (eq x 0) 0 (+ (sumint (- x 1)) x)))", "(sumint 10)"],
            "55",
        ),
    ],
)
def test_compute_if_def(test_inputs: List[str], expected: str) -> None:
    return simple_multi(test_inputs, expected)


@pytest.mark.parametrize(
    "test_inputs,expected",
    [(["(def (fact n) (if (eq n 0) 1 (* n (fact (- n 1)))))", "(fact 10)"], "3628800")],
)
def test_compute_recursive_def(test_inputs: List[str], expected: str) -> None:
    return simple_multi(test_inputs, expected)


@pytest.mark.parametrize(
    "test_inputs,expected", [(["(var x 5) (var y 10) (+ x y)"], "15")]
)
def test_compute_multi_expr(test_inputs: List[str], expected: str) -> None:
    return simple_multi(test_inputs, expected)
