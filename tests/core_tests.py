from typing import Dict, List

import pytest

from llisp.lbuiltins import NotCallable, ParseError, UndefinedError, is_int
from llisp.parser import create_program


def simple_multi(test_inputs: List[str], expected: str) -> None:
    state: Dict[str, object] = {}
    out = None
    for t in test_inputs:
        prog = create_program(t)
        out = prog.run(state).value

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
    assert is_int(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected", [("'1'", "1"), ("'a'", "a"), ("' '", " "), ("'\n'", "\n")]
)
def test_compute_char(test_input: str, expected: str) -> None:
    prog = create_program(test_input)
    assert str(prog.run({}).value) == expected


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
    prog = create_program(test_input)
    assert str(prog.run({}).value) == expected


# Two tests here have been distabled as I am not sure on how I want to
# interpret them
@pytest.mark.parametrize(
    "test_input",
    [
        # "(var)",
        "(var bla bla bla)",
        "(def 5)",
        "(def blah bloh)",
        "(var 'ds')",
        # "(var ))",
    ],
)
def testParseError(test_input: str) -> None:
    with pytest.raises(ParseError):
        prog = create_program(test_input)
        prog.run({})


@pytest.mark.parametrize("test_input", ["(a)", "(var a a)", "(list a b)"])
def testUndefinedError(test_input: str) -> None:
    with pytest.raises(UndefinedError):
        prog = create_program(test_input)
        prog.run({})


@pytest.mark.parametrize(
    "test_input", ["(var a 10) (a 10)", "(var x (list 1 10)) (x 10)"]
)
def testNotCallableError(test_input: str) -> None:
    with pytest.raises(NotCallable):
        prog = create_program(test_input)
        prog.run({})


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("(/ 1 1)", "1.0"),
        ("(/ 1 2)", "0.5"),
        ("(/ 10 5)", "2.0"),
        ("(/ 10 3)", "3.3333333333333335"),
        ("(/ 5.5 2)", "2.75"),
        ("(/ -10 5)", "-2.0"),
        ("(/ 10 -5)", "-2.0"),
    ],
)
def test_compute_divide(test_input: str, expected: str) -> None:
    prog = create_program(test_input)
    assert str(prog.run({}).value) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("(// 1 1)", "1"),
        ("(// 13.5 1)", "13.0"),
        ("(// 1 2)", "0"),
        ("(// 10 5)", "2"),
        ("(// 10 3)", "3"),
        ("(// 5.5 2)", "2.0"),
        ("(// -10 5)", "-2"),
        ("(// 10 -5)", "-2"),
    ],
)
def test_compute_divide_int(test_input: str, expected: str) -> None:
    prog = create_program(test_input)
    assert str(prog.run({}).value) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("(% 1 1)", "0"),
        ("(% 13.5 1)", "0.5"),
        ("(% 1 2)", "1"),
        ("(% 10 5)", "0"),
        ("(% 10 3)", "1"),
        ("(% 5.5 2)", "1.5"),
        ("(% -10 5)", "0"),
        ("(% 10 -5)", "0"),
    ],
)
def test_compute_mod(test_input: str, expected: str) -> None:
    prog = create_program(test_input)
    assert str(prog.run({}).value) == expected


@pytest.mark.skip("The ! operator is not a builtin, but a std")
@pytest.mark.parametrize(
    "test_input,expected", [("(! 1)", "0"), ("(! 0)", "1"), ("(! 10)", "0")]
)
def test_compute_not(test_input: str, expected: str) -> None:
    prog = create_program(test_input)
    assert str(prog.run({}).value) == expected


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
    prog = create_program(test_input)
    assert str(prog.run({}).value) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("(echo 1)", "1"),
        ("(echo 1.)", "1.0"),
        ("(echo '%')", "%"),
        # TODO: possible bug here, we might want to echo "test" or ['t', 'e', 's', 't']
        (
            '(echo "test")',
            "[(AtomTypes.CHAR) t, (AtomTypes.CHAR) e, (AtomTypes.CHAR) s, (AtomTypes.CHAR) t]",
        ),
    ],
)
def test_compute_echo(test_input: str, expected: str) -> None:
    prog = create_program(test_input)
    assert str(prog.run({}).value) == expected


# TODO: the difference between echo and print is... strange
@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("(print 1)", "1"),
        ("(print 1.)", "1.0"),
        ("(print '%')", "%"),
        (
            '(print "test")',
            "[(AtomTypes.CHAR) t, (AtomTypes.CHAR) e, (AtomTypes.CHAR) s, (AtomTypes.CHAR) t]",
        ),
    ],
)
def test_compute_print(test_input: str, expected: str) -> None:
    prog = create_program(test_input)
    assert str(prog.run({}).value) == expected


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
    "test_inputs,expected", [(["(< 1 1)"], "0"), (["(< 2 1)"], "0"), (["(< 1 2)"], "1")]
)
def test_compute_lt(test_inputs: List[str], expected: str) -> None:
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
    "test_inputs,expected",
    [
        (["(var x 5) (var y 10) (+ x y)"], "15"),
        (["(def (albert x) ((var y 10) (+ x y))", "(albert 12)"], "22"),
    ],
)
def test_compute_multi_expr(test_inputs: List[str], expected: str) -> None:
    return simple_multi(test_inputs, expected)


@pytest.mark.parametrize(
    "test_inputs,expected",
    [
        (["(var x (list 1))", "(eq x (list 1))"], "1"),
        (["(var x (list 1))", "(eq x (list 2))"], "0"),
        (["(var x (list 1 2))", "(eq x (list 1 2))"], "1"),
        (["(var x (list 1 2))", "(eq x (list 2 1))"], "0"),
        (["(var a 1)", "(var x (list a 2))", "(eq x (list 1 2))"], "1"),
    ],
)
def test_compute_list(test_inputs: List[str], expected: str) -> None:
    return simple_multi(test_inputs, expected)


@pytest.mark.parametrize(
    "test_inputs,expected",
    [
        (['(var x "a"', "(eq x (list 'a'))"], "1"),
        (['(var x "abcd"', "(eq x (list 'a' 'b' 'c' 'd'))"], "1"),
        (['(var x "ab d"', "(eq x (list 'a' 'b' ' ' 'd'))"], "1"),
    ],
)
def test_compute_str(test_inputs: List[str], expected: str) -> None:
    return simple_multi(test_inputs, expected)
