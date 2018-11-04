#!/usr/bin/env python3
# coding: utf-8

import argparse
import os
from typing import Dict

from llisp.parser import listing


def execute_file(filename: str, state: Dict, debug=False) -> int:
    with open(filename, "r") as script_file:
        script = script_file.read()
        e = listing(script, None)
        if debug:
            print(f"EXPR::{e}")
        e.evaluate(state)
        return 0


def main() -> int:
    state: Dict[str, str] = {}

    # LOAD STD LSL (Loïc Standard Library)
    STD_PATH = os.path.join(os.path.dirname(__file__), "std.lisp")
    execute_file(STD_PATH, state)

    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?", default="")
    args = parser.parse_args()
    if args.file:
        return execute_file(args.file, state)

    print("Welcome to Loïc Lisp interpreter (llisp)")
    print("Type exit to exit")
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
