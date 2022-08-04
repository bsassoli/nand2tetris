import sys
import os
from typing import List
from textwrap import dedent
from parser import Parser
from codeWriter import CodeWriter

def open_file() -> List[str]:
    """Opens file and returns list of lines"""
    try:
        path = sys.argv[1]
    except IndexError:
        print("ERROR: You must provide a filename as an argument")
        print("*" * 48)
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
    fileOutName = os.path.basename(sys.argv[1]).split(".")[0] + ".asm"
    dirOutName = os.path.dirname(sys.argv[1])
    write_path = os.path.join(dirOutName, fileOutName)
    writer = CodeWriter(fileOutName, write_path)
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() in ["C_PUSH", "C_POP"]:
            segment = parser.arg1()
            index = parser.arg2()
            writer.writePushPop(parser.command_type(), segment, index)
        if parser.command_type() == "C_ARITHMETIC":
            writer.writeArithmetic(parser.current_command)
    writer.close()


if __name__ == "__main__":
    main()
