from utils import collate_instructions

# If is_directory

class CodeWriter():
    def __init__(self, file_name, write_path) -> None:
        """Init for CodeWriter class"""
        if "." in file_name:
            self.file_name = file_name.split(".")[0]
        else:
            self.file_name = file_name
        #self.file = open(write_path, "w")
        self.jump = 0
        self.current_func = ""
        self.function_dict = {}
        print("Current filename: " + self.file_name)

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
        outstring = comment
        outstring += collate_instructions(instructions)        
        outstring = "\n".join(instructions)
        outstring += "\n"
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

        outstring += collate_instructions(instructions)
        return outstring

    def close(self) -> None:
        """Closes file when translation is completed"""
        self.file.close()

    def write_init(self) -> str:
        """Initializes .asm file with bootstrap code"""
        instructions = [
        "// init", 
        "@256", 
        "D=A",
        "@SP",
        "M=D"]
        outstring = collate_instructions(instructions)
        outstring += self.write_call("Sys.init", 0)
        return outstring

    def write_label(self, label_name: str) -> str:
        """Handles translation of labels"""
        outstring = f"({self.file_name}.{self.current_func}${label_name})\n"
        return outstring

    def write_goto(self, label_name: str) -> str:
        """Handles translation of goto instructions"""
        outstring = f"@{self.file_name}.{self.current_func}${label_name}\n"
        outstring += "0;JMP\n"
        return outstring

    def write_if(self, label_name: str) -> str:
        """Handles translation of if-goto instructions"""
        instructions = [
            "@SP",
            "AM=M-1",
            "D=M",
            f"@{self.file_name}.{self.current_func}${label_name}",
            "D;JNE",
        ]
        outstring = collate_instructions(instructions)
        return outstring

    def write_call(self, function_name: str, n_args: int) -> str:
        """Handles translation of call instructions"""
        instructions = [f"// call {function_name} {n_args}"]
        function_name = self.file_name + "." + function_name
        PUSH = [
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        ]  # str constant that pushes what's in D-regoster on stack
        # push retAddrLabel Using a translator-generated label
        if function_name in self.function_dict:
            ret_address_label = self.function_dict[function_name]
        else:
            ret_address_label = len(self.function_dict)
            self.function_dict[function_name] = ret_address_label

        instructions += [
            f"@{function_name}$return{ret_address_label}",
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
        # ARG = SP-5-nArgs
        instructions += [
            "@SP",
            "D=M",
            "@5",
            "D=D-A",
            "@" + str(n_args),
            "D=D-A",
            "@ARG",
            "M=D",
        ]
        # LCL = SP
        instructions += ["@SP", "D=M", "@LCL", "M=D"]
        # goto functionName
        instructions += [f"@{function_name}"]
        instructions += ["0;JMP"]
        # (retAddrLabel) the same translator-generated label
        instructions += [f"({function_name}$return{ret_address_label})"]
        outstring = collate_instructions(instructions)
        return outstring

    def write_function(self, function_name: str, n_vars: int) -> str:
        """Handles translation of C_FUNCTION"""
        # generate label
        instructions = [f"// function {function_name} {n_vars}"]
        function_name = self.file_name + "." + function_name
        instructions += [f"({function_name})"]
        # repeat n_vars times:
        # push local 0
        while n_vars > 0:
            instructions += ["D=0", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
            n_vars -= 1
        outstring = collate_instructions(instructions)
        return outstring

    def write_return(self) -> str:
        """Handles translation of return command"""
        # endFrame = LCL
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
            "@R14",
            "M=D",
            # STAR*ARG = pop()
            "@SP",
            "AM=M-1",
            "D=M",
            "@ARG",
            "A=M",
            "M=D",
            # SP = ARG + 1
            "@ARG",
            "D=M+1",
            "@SP",
            "M=D",
            # THAT = *(endFrame - 1)
            "@R13",
            "A=M-1",
            "D=M",
            "@THAT",
            "M=D",
            # THIS = *(endFrame - 2)
            "@2",
            "D=A",
            "@R13",
            "A=M-D",
            "D=M",
            "@THIS",
            "M=D",
            # ARG = *(endFrame - 3)
            "@3",
            "D=A",
            "@R13",
            "A=M-D",
            "D=M",
            "@ARG",
            "M=D",
            # LCL = *(endFrame - 4)
            "@4",
            "D=A",
            "@R13",
            "A=M-D",
            "D=M",
            "@LCL",
            "M=D",
            # goto retAddr
            "@R14",
            "A=M",
            "0;JMP",
        ]
        outstring = "// return\n"
        outstring += collate_instructions(instructions)
        return outstring
