""" Main script that preprocesses, opens files\n
and instantiates both Parser and Codewriter to perform\n
translation from .vm to .asm.
"""
import sys
import os
import pathlib

from typing import Union, Tuple, List
from textwrap import dedent
from parser import Parser
from codeWriter import CodeWriter
from utils import write_output

Path = Union[str, pathlib.Path]


def dir_or_file(path: Path) -> Tuple[str, str]:
    """dir_or_file checks if supplied path is a directory or a file

    Returns:
        Tuple[str, str]: "dir" or "file" or raises an exception and the destination basename

    """
    if os.path.isdir(path):
        name = os.path.dirname(path).split("/")[-1]
        return "dir", name
    if os.path.isfile(path):
        name = os.path.dirname(path).split(".")[0]
        return "file", name
    return path + " is neither a file nor a valid directory."


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


def translate_file(
    filename: Path,
    outname: str,
    bootstrap: bool = False,
    is_dir: bool = False,
    function_count: int = 1,
) -> None:
    """translate_file Given a path to a .vm file creates a .asm translation of its contents

    Args:
        filename (Path): the file to be translated
        outname (str): the file to be written
    """
    lines = open_file(filename)
    lines = preprocess(lines)
    parser = Parser(lines)
    file_out_name = outname + ".asm"
    dir_out_name = os.path.dirname(filename)
    if is_dir:
        write_path = dir_out_name + ".asm"
    else:
        write_path = file_out_name
    writer = CodeWriter(outname, write_path, function_count)
    writer.set_filename(os.path.split(filename.split(".")[0])[-1])
    out = ""
    if bootstrap:
        out += writer.write_init()
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() in ["C_PUSH", "C_POP"]:
            segment = parser.arg1()
            index = parser.arg2()
            out += writer.write_push_pop(parser.command_type(), segment, index)
        if parser.command_type() == "C_ARITHMETIC":
            out += writer.write_arithmetic(parser.current_command)
        if parser.command_type() == "C_LABEL":
            out += writer.write_label(parser.arg1())
        if parser.command_type() == "C_GOTO":
            out += writer.write_goto(parser.arg1())
        if parser.command_type() == "C_IF":
            out += writer.write_if(parser.arg1())
        if parser.command_type() == "C_CALL":
            out += writer.write_call(parser.arg1(), int(parser.arg2()))
        if parser.command_type() == "C_FUNCTION":
            out += writer.write_function(parser.arg1(), int(parser.arg2()))
        if parser.command_type() == "C_RETURN":
            out += writer.write_return()
    return out, writer.function_count


def main():
    path = sys.argv[1]
    operation_type, outname = dir_or_file(path)
    out = ""
    if operation_type == "file":
        out += translate_file(
            path, outname, bootstrap=False, is_dir=False, function_count=1
        )[0]
        out_path = os.path.basename(path).split(".")[0] + ".asm"
    else:
        boostrap = True
        prev_function_count = 1
        for file in os.listdir(path):
            if os.path.basename(file).split(".")[1] == "vm":
                target = os.path.join(path, file)
                new, new_function_count = translate_file(
                    target,
                    outname,
                    bootstrap=boostrap,
                    is_dir=True,
                    function_count=prev_function_count,
                )
                out += new
                boostrap = False
                prev_function_count = new_function_count

        out_path = os.path.split(os.path.abspath(path))[1] + ".asm"

    head, tail = os.path.split(os.path.abspath(path))
    if operation_type == "dir":
        out_path = os.path.join(head, tail, out_path)
    else:
        out_path = os.path.join(head, out_path)
    write_output(out, out_path)


if __name__ == "__main__":
    main()
