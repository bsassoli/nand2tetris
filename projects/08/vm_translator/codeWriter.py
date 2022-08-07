class CodeWriter:
    def __init__(self, file_name, write_path) -> None:
        """Init for CodeWriter class"""
        self.file_name = file_name
        file = open(write_path, "w")
        self.file = file
        self.jump = 0
        self.current_func = ""
        self.function_dict = {}

    def write_arithmetic(self, command: str) -> str:
        """Handles translation arithmetic commands"""
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
        comment = f"//{command}\n"
        self.file.write(comment)
        outstring += "\n".join(instructions)
        outstring += "\n"
        self.file.write(outstring)
        return outstring

    def write_push_pop(self, command: str, segment: str, index: int) -> str:
        """Handles translation of push and pop commands"""
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
                    f"@{self.file_name}.{index}",
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
                    f"@{self.file_name}.{index}",
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
        """Closes file when translation is completed"""
        self.file.close()

    def write_init(self) -> None:
        """Initializes .asm file"""
        outstring = "// init\n"
        outstring += "@256\n"
        outstring += "D=A\n"
        outstring += "@SP\n"
        outstring += "M=D\n"
        # outstring += "call Sys.init 0\n"
        self.file.write(outstring)

    def write_label(self, label_name: str) -> None:
        """Handles translation of labels"""
        outstring = f"({self.file_name}.{self.current_func}${label_name})\n"
        self.file.write(outstring)

    def write_goto(self, label_name: str) -> None:
        """Handles translation of goto instructions"""
        outstring = f"@{self.file_name}.{self.current_func}${label_name}\n"
        outstring += "0;JMP\n"
        self.file.write(outstring)

    def write_if(self, label_name: str) -> None:
        """Handles translation of if-goto instructions"""
        instructions = [
            "@SP",
            "AM=M-1",
            "D=M",
            f"@{self.file_name}.{self.current_func}${label_name}",
            "D;JNE",
        ]
        outstring = "\n".join(instructions) + "\n"
        self.file.write(outstring)

    def write_call(self, function_name: str, n_args: int) -> None:
        """Handles translation of call instructions"""
        instructions = [f"// call {function_name} {n_args}"]
        function_name = self.file_name+"."+function_name
        print(function_name, n_args)
        PUSH = ["@SP",
                "A=M"
                "M=D",
                "@SP",
                "M=M+1"] # str constant that pushes what's in D-regoster on stack
        # push retAddrLabel Using a translator-generated label
        if function_name in self.function_dict:
            ret_address_label = self.function_dict[function_name]
        else:
            ret_address_label = len(self.function_dict)
            self.function_dict[function_name] = ret_address_label
        
        instructions += [            
            f"@{function_name}$return{ret_address_label}",
            "D=A",]
        instructions += PUSH
        # push LCL
        instructions += ["@LCL", "D=M"]
        instructions += PUSH
        # push ARG
        instructions += ["@ARG", "D=M"]
        instructions += PUSH
        # push THIS
        instructions += ["@THIS", "D=M"]
        # push THAT
        instructions += ["@THAT", "D=M"]
        # ARG = SP-5-nArgs
        instructions += [
            "@SP",
            "D=M",
            "@5",
            "D=D-A",
            "@"+n_args,
            "D=D-A",
            "@ARG",
            "M=D"]
        # LCL = SP
        instructions += [
            "@SP",
            "D=M",
            "@LCL",
            "M=D"
        ]
        # goto functionName
        instructions += f"@{function_name}"
        instructions += "0;JMP"
        # (retAddrLabel) the same translator-generated label
        instructions += f"(@{function_name}$return{ret_address_label})"
        outstring = ("\n").join(instructions) + "\n"
        print(outstring)
        self.file.write(outstring)
