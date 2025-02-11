import sys

from .bril import Program


def read_std_in() -> Program:
    return Program.model_validate_json("".join(line for line in sys.stdin), strict=True)
