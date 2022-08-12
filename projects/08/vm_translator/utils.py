"""helper functions for CodeWriter and Parser classes"""
import pathlib
from typing import List, Union

destfile = Union[str, pathlib.Path]


def collate_instructions(instructions: List[str]) -> str:
    """collate_instructions generates a string of commands
    separated by newlines and terminating with a newline

    Args:
        instructions (List[str]): a list of commands

    Returns:
        str: a string
    """
    return ("\n").join(instructions) + "\n"


def write_output(outstring: str, dest: destfile) -> None:
    """Writes commands to file"""
    with open(dest, "w") as destination:
        destination.write(outstring)
