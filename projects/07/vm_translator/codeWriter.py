class CodeWriter():
    def __init__(self, fileName, write_path) -> None:
        self.fileName = fileName
        file = open(write_path, "w")
        self.file = file
        self.jump = 0

    def writeArithmetic(self, command: str) -> str:
        outstring = f"//{command}\n"
        if command in ["add", "sub"]:
            instructions = ["@SP", "M=M-1", "A=M", "D=M", "A=A-1"]
            if command == "add":
                instructions.append("M=D+M")
            else:
                instructions.append("M=M-D")
        elif command == "neg":
            instructions = ["@SP", "A=M-1", "M=-M"]
        elif command == "not":
            instructions = ["@SP", "A=M-1", "M=!M"]
        elif command == "or":
            instructions = ["@SP", "M=M-1", "A=M", "D=M", "A=A-1", "M=D|M"]
        elif command == "and":
            instructions = ["@SP", "M=M-1", "A=M", "D=M", "A=A-1", "M=D&M"]
        elif command in ["eq", "gt", "lt"]:
            comparisons = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}
            instructions = [
                "@SP",
                "M=M-1",
                "A=M",
                "D=M",
                "A=A-1",
                "D=M-D",
                "M=-1",
                f"@J_{self.jump}",
                f"D;{comparisons[command]}",
                "@SP",
                "A=M-1",
                "M=0",
                f"(J_{self.jump})",
            ]
            self.jump += 1
        outstring += "\n".join(instructions)
        outstring += "\n"
        self.file.write(outstring)
        return outstring

    def writePushPop(self, command: str, segment: str, index: int) -> str:
        segment_dict = {
            "local": "LCL",
            "this": "THIS",
            "that": "THAT",
            "argument": "ARG",
        }
        outstring = f"//{command} {segment} {index}\n"
        if command == "C_PUSH":
            if segment == "constant":
                instructions = [f"@{index}", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
            elif segment == "static":
                instructions = [
                    f"@{self.fileName}.{index}",
                    "D=M",
                    "@SP",
                    "A=M",
                    "M=D",
                    "@SP",
                    "M=M+1",
                ]
            elif segment == "temp":
                instructions = [
                    f"@{index}",
                    "D=A",
                    "@R5",
                    "A=D+A",
                    "D=M",
                    "@SP",
                    "A=M",
                    "M=D",
                    "@SP",
                    "M=M+1",
                ]
            elif segment == "pointer":
                if index == "0":
                    this_or_that = "THIS"
                elif index == "1":
                    this_or_that = "THAT"
                instructions = [
                    f"@{this_or_that}",
                    "D=M",
                    "@SP",
                    "A=M",
                    "M=D",
                    "@SP",
                    "M=M+1",
                ]
            elif segment in ["argument", "local", "this", "that"]:
                segment = segment_dict[segment]
                instructions = [
                    f"@{segment}",
                    "D=M",
                    f"@{index}",
                    "A=D+A",
                    "D=M",
                    "@SP",
                    "A=M",
                    "M=A",
                    "M=D",
                    "@SP",
                    "M=M+1",
                ]
            else:
                raise Exception("No such memory segment: " + segment)

        elif command == "C_POP":
            if segment == "static":
                instructions = [
                    "@SP",
                    "A=M-1",
                    "D=M",
                    f"@{self.fileName}.{index}",
                    "M=D",
                    "@SP",
                    "M=M-1",
                ]
            elif segment == "temp":
                instructions = [
                    f"@{5}",
                    "D=A",
                    f"@{index}",
                    "D=D+A",
                    "@R13",
                    "M=D",
                    "@SP",
                    "M=M-1",
                    "D=M",
                    "@R15",
                    "M=D",
                    "A=M",
                    "D=M",
                    "M=D",
                    "@R13",
                    "A=M",
                    "M=D",
                ]
            elif segment == "pointer":
                if index == "0":
                    this_or_that = "THIS"
                elif index == "1":
                    this_or_that = "THAT"
                instructions = ["@SP", "M=M-1", "A=M", "D=M", f"@{this_or_that}", "M=D"]
            elif segment in ["argument", "local", "this", "that"]:
                segment = segment_dict[segment]
                instructions = [
                    f"@{segment}",
                    "D=M",
                    f"@{index}",
                    "D=D+A",
                    "@R13",
                    "M=D",
                    "@SP",
                    "M=M-1",
                    "D=M",
                    "@R15",
                    "M=D",
                    "A=M",
                    "D=M",
                    "M=D",
                    "@R13",
                    "A=M",
                    "M=D",
                ]
            else:
                raise Exception("No such memory segment: " + segment)
        else:
            raise Exception("No such command type: " + command)

        outstring += "\n".join(instructions)
        outstring += "\n"
        self.file.write(outstring)
        return outstring

    def close(self) -> None:
        self.file.close()
