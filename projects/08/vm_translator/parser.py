""" Implements the Parser class. Given a list of instructions as string, returns the parsed strings.
"""

from typing import List


class Parser:
    """ Parser class takes a list of string and parses them
    """

    def __init__(self, file: List[str]):

        if len(file):
            self.file = file
        else:
            raise Exception("No contents in file")
        self.current_line = 0
        self.current_command = ""
        self.next_command = ""
        self.is_arithmetic = ["add", "sub", "neg", "eq", "gt", "lt", "or", "and", "not"]
        self.commands_dict = {
            "push": "C_PUSH",
            "pop": "C_POP",
            "label": "C_LABEL",
            "goto": "C_GOTO",
            "if-goto": "C_IF",
            "function": "C_FUNCTION",
            "return": "C_RETURN",
            "call": "C_CALL",
        }

    def __str__(self):
        pass

    def has_more_commands(self) -> bool:
        return self.current_line <= len(self.file) - 1

    def advance(self) -> None:
        if self.has_more_commands():
            self.next_command = self.file[self.current_line]
        self.current_line += 1
        self.current_command = self.next_command

    def command_type(self):
        ctype = self.current_command.split()[0]
        if self.current_command in self.is_arithmetic:
            return "C_ARITHMETIC"
        if ctype in self.commands_dict:
            return self.commands_dict[ctype]
        raise Exception(f"No such command type: {ctype}")

    def arg1(self):
        if self.command_type() == "C_ARITHMETIC":
            return self.current_command
        assert (
            self.command_type() != "C_RETURN"
        ), "self.arg1() should not be called with C_RETURN command types"
        return self.current_command.split()[1]

    def arg2(self):
        assert self.command_type() in [
            "C_PUSH",
            "C_POP",
            "C_CALL",
            "C_FUNCTION",
        ], "self.arg2() called with wrong command type"
        return self.current_command.split()[2]
