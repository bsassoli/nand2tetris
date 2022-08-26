""" Parses a file containig a program in .asm format and writes a .hack file.
File to be parsed should be specified as argument.
Usage: python parser.py filename
"""

from textwrap import dedent
from typing import List, Dict
import sys
import os

from mappings import CMP_TABLE, DST_TABLE, JMP_TABLE
from symbol_table import SYMBOL_TABLE
from utils import get_binary


def get_lines(name_of_file: str) -> List[str]:
    """get_lines opens files and returns lines as list of strs
    """
    filepath = os.path.join(os.getcwd(), name_of_file)
    with open(filepath, "r") as file:
        instructions = file.readlines()
    return instructions


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
    assert all(" " not in inline for inline in lines), "Whitespace present"

    return lines


def first_pass(program: List[str], symbol_table: Dict[str, int]) -> Dict[str, int]:
    """first_pass constructs mappings for labels

    Args:
        program (List[str]): the program to be parsed
        symbol_table (str, int): a (possibly empty)
                                dict representing the existing mappings

    Returns:
        Dict[str, int]: a mapping from label symbols to addresses
    """

    counter = 0
    for line in program:
        if line[0] == "(":
            if line[1:-1] in symbol_table:
                pass
            else:
                symbol_table[line[1:-1]] = counter
                counter -= 1
        counter += 1
    program = [instr for instr in program if instr[0] != "("]
    return symbol_table, program


def second_pass(program: List[str], symbol_table: Dict[str, int]) -> Dict[str, int]:
    """second_pass Construct mappings for variables

    Args:
        program (List[str]): the program to be parsed
        symbol_table (str, int): a (possibly empty)
                                dict representing the existing mappings

    Returns:
        Dict[str, int]: a mapping from variable symbols to addresses
    """
    counter = 16
    for line in program:
        if line in symbol_table:
            pass
        if line[0] == "@" and line[1] != "R" and not line[1].isnumeric():
            if line[1:] not in symbol_table:
                symbol_table[line[1:]] = counter
                counter += 1
    return symbol_table


def parse(
    line: str,
    cmp_table: Dict[str, str],
    dst_table: Dict[str, str],
    jmp_table: Dict[str, str],
    symbol_table: Dict[str, int],
) -> str:
    """parse converts a line from the Assembly language
    to a string representing a binary HACK machine language
    instruction.

    Args:
        line (str): The assembly instruction to parse
        cmp_table (Dict[str, str]): maps comp instructions to cmp bits
        dst_table (Dict[str, str]): maps dst instructions to dst bits
        jmp_table (Dict[str, str]): maps comp instructions to jmp bits
        symbol_table: Dict[str, int]: maps symbols to adresses

    Returns:
        str: a string representing the 16-bit machine language translation.
    """
    lineout = ["" for _ in range(16)]
    if line[0] == "(":  # Label
        pass
    # Decide if A- or C-instruction?
    if line[0] == "@":  # A-instruction
        # lineout = > 0 + binary representation of what follows
        if line[1:] not in symbol_table:
            address = get_binary(int(line[1:]), 15)
            lineout = "0" + address
            return lineout
        address = symbol_table[line[1:]]
        return "0" + get_binary(address, 15)
    # C-instruction
    lineout[0:3] = "111"
    # Either the dest or jump fields may be empty.
    # If dest is empty, '=' is omitted
    # If jump is empty, ';' is omitted.
    if ";" in line and "=" in line:
        dst, _ = line.split("=")
        cmp, jmp = line.split(";")
    elif ";" not in line:
        jmp = "null"
        dst, cmp = line.split("=")
    else:
        dst = "null"
        cmp, jmp = line.split(";")
    lineout[13:16] = jmp_table[jmp]
    lineout[10:13] = dst_table[dst]
    # convert comp bit
    if "M" in cmp:
        lineout[3] = "1"
    else:
        lineout[3] = "0"

    lineout[4:10] = cmp_table[cmp]
    assert len(lineout) == 16, "Output isn't 16 bits"
    return ("").join(lineout)


def main():
    """parses file and writes output in .hack format
    """
    try:
        path = sys.argv[1]
    except IndexError:
        print("ERROR: You must provide a filename as an argument")
        print("*" * 48)
    filename = os.path.basename(path).split(".")[0]
    assert filename + ".asm" in os.listdir(
        os.path.dirname(path)
    ), f"ERROR: No file called '{filename}.asm' found"
    inlines = get_lines(path)
    inlines = preprocess(inlines)
    symbol_map, inlines = first_pass(inlines, SYMBOL_TABLE)
    symbol_map = second_pass(inlines, SYMBOL_TABLE)
    outlines = []
    for _, instr in enumerate(inlines):
        parsed = parse(instr, CMP_TABLE, DST_TABLE, JMP_TABLE, symbol_map)
        outlines.append(parsed + "\n")
    destination_file = filename + ".hack"
    with open(destination_file, "w") as fout:
        fout.writelines(outlines)


if __name__ == "__main__":
    main()
