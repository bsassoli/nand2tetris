class Parser():

    def __init__(self, file):
        self.file = file
        self.line = ""
        self.currentCommand = ""
        self.nextCommand = ""
        self.arithmetic = ["add", "sub", "eq", "neg", "gt", "and", "not"]
        self.commandsDict = {
            "push": "C_PUSH",
            "pop": "C_POP",
            "label": "C_LABEL",
            "goto": "C_GOTO",
            "if": "C_IF",
            "function": "C_FUNCTION",
            "return": "C_RETURN",
            "call": "C_CALL"
        }

    def hasMoreCommands(self) -> bool:
        return self.nextCommand

    def advance(self) -> None:
        if self.hasMoreCommands():
            self.currentCommand = self.nextCommand

    def commandType(self):
        ctype = self.currentCommand.split()[0]
        if ctype in self.arithmetic:
            return "C_ARITHMETIC"
        if ctype in self.commandsDict:
            return self.commandsDict[ctype]
        raise Exception("Non such command type.")

    def arg1(self):
        return self.currentCommand.split()[1]

    def arg2(self):
        return self.currentCommand.split()[2]
