from utils import collate_instructions


class CodeWriter:
    def __init__(self, file_name, function_count) -> None:
        """Init for CodeWriter class"""
        if "." in file_name:
            self.file_name = file_name.split(".")[0]
        else:
            self.file_name = file_name
        # self.file = open(write_path, "w")
        self.jump = 0
        self.current_func = ""
        self.function_count = function_count

    def set_filename(self, name) -> None:
        self.file_name = name

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
                "@SP",
                "A=M",
                "D=M",
                "@SP",
                "M=M-1",
                "@SP",
                "A=M",
                "D=M-D",
                f"@BOOL_START_{self.jump}",
                f"D;{comparisons[command]}",
                "@SP",
                "A=M",
                "M=0",
                f"@BOOL_END_{self.jump}",
                "0;JMP",
                f"(BOOL_START_{self.jump})",
                "@SP",
                "A=M",
                "M=-1",
                f"(BOOL_END_{self.jump})",
                "@SP",
                "M=M+1",
            ]
            self.jump += 1
        comment = f"//{command}\n"
        outstring = comment
        outstring += collate_instructions(instructions)
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
                    "A=D+A",
                    "D=A",
                    "@R13",
                    "M=D",
                    "@SP",
                    "M=M-1",
                    "@SP",
                    "A=M",
                    "D=M",
                    "@R13",
                    "A=M",
                    "M=D",
                ]
            else:
                raise Exception("No such memory segment: " + segment)
        else:
            raise Exception("No such command type: " + command)

        outstring += collate_instructions(instructions)
        return outstring

    def write_init(self) -> str:
        """Initializes .asm file with bootstrap code"""
        instructions = ["// init", "@256", "D=A", "@SP", "M=D"]
        outstring = collate_instructions(instructions)
        outstring += self.write_call("Sys.init", 0)
        return outstring

    def write_label(self, label_name: str) -> str:
        """Handles translation of labels"""
        outstring = f"// label {label_name}\n"
        if self.current_func:
            outstring += f"({self.current_func}${label_name})\n"
        else:
            outstring += f"({label_name})\n"
        return outstring

    def write_goto(self, label_name: str) -> str:
        """Handles translation of goto instructions"""
        outstring = f"// goto {label_name}\n"
        if self.current_func:
            outstring += f"@{self.current_func}${label_name}\n"
        else:
            outstring += f"@{label_name}\n"
        outstring += "0;JMP\n"
        return outstring

    def write_if(self, label_name: str) -> str:
        """Handles translation of if-goto instructions"""
        instructions = [f"// if-goto {label_name}"]
        instructions += ["@SP", "M=M-1", "@SP", "A=M", "D=M"]
        if self.current_func:
            instructions += [f"@{self.current_func}${label_name}"]
        else:
            instructions += [f"@{label_name}"]
        instructions += ["D;JNE"]
        outstring = collate_instructions(instructions)
        return outstring

    def write_call(self, function_name: str, n_args: int) -> str:
        """Handles translation of call instructions"""
        instructions = [f"// call {function_name} {n_args}"]
        PUSH = [
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        ]  # str constant that pushes what's in D-regoster on stack
        # push retAddrLabel Using a translator-generated label

        ret_address_label = str(self.function_count)

        instructions += [
            f"@{function_name}${ret_address_label}",
            "D=A",
        ]
        instructions += PUSH
        # push LCL
        instructions += ["@LCL", "D=M"]
        instructions += PUSH
        # push ARG
        instructions += ["@ARG", "D=M"]
        instructions += PUSH
        # push THIS
        instructions += ["@THIS", "D=M"]
        instructions += PUSH
        # push THAT
        instructions += ["@THAT", "D=M"]
        instructions += PUSH

        # LCL = SP
        instructions += [
            "@SP",
            "D=M",
            "@LCL",
            "M=D",
        ]
        # ARG = SP-5-nArgs
        instructions += [f"@{str(n_args + 5)}", "D=D-A", "@ARG", "M=D"]
        # goto functionName
        instructions += [f"@{function_name}"]
        instructions += ["0;JMP"]
        # (retAddrLabel) the same translator-generated label
        instructions += [f"({function_name}${ret_address_label})"]
        outstring = collate_instructions(instructions)
        self.function_count += 1
        return outstring

    def write_function(self, function_name: str, n_vars: int) -> str:
        """Handles translation of C_FUNCTION"""
        self.current_func = function_name
        # generate label
        instructions = [f"// function {function_name} {n_vars}"]
        # function_name = self.file_name + "." + function_name
        instructions += [f"({function_name})"]
        # repeat n_vars times:
        # push local 0
        while n_vars > 0:
            instructions += ["@SP", "A=M", "M=0", "@SP", "M=M+1"]
            n_vars -= 1
        outstring = collate_instructions(instructions)
        return outstring

    def write_return() -> str:
        """Handles translation of return command"""
        # endFrame = LCL
        outstring = "// return\n"
        instructions = [
            # endofframe temp var =  address of LCL
            "@LCL",
            "D=M",
            "@R13",
            "M=D",
            # retAddr = *(endFrame - 5) // gets the return address
            "@R13",
            "D=M",
            "@5",
            "D=D-A",
            "A=D",
            "D=M",
            "@R14",
            "M=D",
            # STAR*ARG = pop()
            "@SP",
            "M=M-1",
            "@SP",
            "A=M",
            "D=M",
            "@ARG",
            "A=M",
            "M=D",
            # SP = ARG + 1
            "@ARG",
            "D=M",
            "@SP",
            "M=D+1",
        ]
        for ix, addr in enumerate(["@THAT", "@THIS", "@ARG", "@LCL"], start=1):
            reset = ["@R13", "D=M"]
            reset += ["@" + str(ix)]
            reset += ["D=D-A", "A=D", "D=M"]
            reset += [addr]
            reset += ["M=D"]
            instructions += reset
        # goto retAddr
        instructions += ["@R14", "A=M", "0;JMP"]
        outstring += collate_instructions(instructions)
        return outstring
