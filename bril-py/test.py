from pydantic import ValidationError

from util import read_std_in
from bril import Program


def main():
    try:
        program: Program = read_std_in()
        # print(program)
        print("Program successfully parsed.")
    except ValidationError as e:
        print(e.errors()[0])


if __name__ == "__main__":
    main()