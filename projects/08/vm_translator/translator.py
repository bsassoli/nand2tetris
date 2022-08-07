""" Main script that preprocess, opens files\n
and instantiates both Parser and Codewriter to perform\n
translation from .vm to .asm.
"""
import sys
import os
import pathlib
from typing import List, Union
from textwrap import dedent
from parser import Parser
from codeWriter import CodeWriter


Path = Union[str, pathlib.Path]


def dir_or_file(path: Path) -> str:
    """dir_or_file checks if supplied path is a directory or a file

    Returns:
        str: "dir" or "file" or raises an exception
    """
    if os.path.isdir(path):
        return "dir"
    if os.path.isfile(path):
        return "file"
    return path + "is neither a file nor a valid directory."


def open_file(path: Path) -> List[str]:
    """Opens file and returns list of lines"""
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


def translate_file(filename: Path, bootstrap=False) -> None:
    """translate_file Given a path to a .vm file creates a .asm translation of its contents

    Args:
        filename (Path): the file to be translated
    """
    lines = open_file(filename)
    lines = preprocess(lines)
    parser = Parser(lines)
    file_out_name = os.path.basename(filename).split(".")[0] + ".asm"
    dir_out_name = os.path.dirname(filename)
    write_path = os.path.join(dir_out_name, file_out_name)
    writer = CodeWriter(file_out_name, write_path)
    if bootstrap:
        writer.write_init()
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() in ["C_PUSH", "C_POP"]:
            segment = parser.arg1()
            index = parser.arg2()
            writer.write_push_pop(parser.command_type(), segment, index)
        if parser.command_type() == "C_ARITHMETIC":
            writer.write_arithmetic(parser.current_command)
        if parser.command_type() == "C_LABEL":
            writer.write_label(parser.arg1())
        if parser.command_type() == "C_GOTO":
            writer.write_goto(parser.arg1())
        if parser.command_type() == "C_IF":
            writer.write_if(parser.arg1())
        if parser.command_type() == "C_CALL":
            writer.write_call(parser.arg1(), int(parser.arg2()))
        if parser.command_type() == "C_FUNCTION":
            writer.write_function(parser.arg1(), int(parser.arg2()))
        if parser.command_type() == "C_RETURN":
            writer.write_return()

    print(f"Writing file: '{file_out_name}'")
    writer.close()


def main():
    path = sys.argv[1]
    operation_type = dir_or_file(path)
    print("Path for translator " + path)
    if operation_type == "file":
        translate_file(path, bootstrap=False)
    else:
        for file in os.listdir(path):
            if os.path.basename(file).split(".")[1] == "vm":
                target = os.path.join(path, file)
                translate_file(target, bootstrap=True)
        
if __name__ == "__main__":
    main()
