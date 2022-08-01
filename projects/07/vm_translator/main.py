import sys
import os
from typing import List
from textwrap import dedent
from parser import Parser


def open_file() -> List[str]:
    """Opens file and returns list of lines"""
    try:
        path = sys.argv[1]
    except IndexError:
        print("ERROR: You must provide a filename as an argument")
        print("*"*48)
    print(os.path.basename(path))
    filename = os.path.basename(path).split(".")[0]
    assert filename + ".vm" in os.listdir(
        os.path.dirname(path)
    ), f"ERROR: No file called '{filename}.vm' found"
    with open(path, "r") as file:
        program = file.readlines()
    return program


def preprocess(lines: List[str]) -> List[str]:
    """Given a list of strings returns the same list without whitespaces,
        indentation, inline comments or line comments.
    """
    # Remove whitespace and indentation
    lines = [dedent(line).strip() for line in lines]
    # Remove comments
    lines = [line for line in lines if line[:2] != "//"]  # line comments
    lines = [line.split("//")[0].strip() for line in lines]  # inline comments
    # Remove empty lines
    lines = [line for line in lines if line != ""]
    # assert all(" " not in inline for inline in lines), "Whitespace present"

    return lines


def main():
    lines = open_file()
    lines = preprocess(lines)
    parser = Parser(lines)
    print(lines)

if __name__ == "__main__":
    main()
    
