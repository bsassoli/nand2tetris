// function Class1.set 0
(Class1.asm.Class1.set)
//C_PUSH argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=A
M=D
@SP
M=M+1
//C_POP static 0
@SP
A=M-1
D=M
@Class1.asm.0
M=D
@SP
M=M-1
//C_PUSH argument 1
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=A
M=D
@SP
M=M+1
//C_POP static 1
@SP
A=M-1
D=M
@Class1.asm.1
M=D
@SP
M=M-1
//C_PUSH constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// return
@LCL
D=M
@R13
M=D
@R13
D=M
@5
D=D-A
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
A=M-1
D=M
@THAT
M=D
@2
D=A
@R13
A=M-D
D=M
@THIS
M=D
@3
D=A
@R13
A=M-D
D=M
@ARG
M=D
@4
D=A
@R13
A=M-D
D=M
@LCL
M=D
@R14
A=M
0;JMP
// function Class1.get 0
(Class1.asm.Class1.get)
//C_PUSH static 0
@Class1.asm.0
D=M
@SP
A=M
M=D
@SP
M=M+1
//C_PUSH static 1
@Class1.asm.1
D=M
@SP
A=M
M=D
@SP
M=M+1
//sub
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D
// return
@LCL
D=M
@R13
M=D
@R13
D=M
@5
D=D-A
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
A=M-1
D=M
@THAT
M=D
@2
D=A
@R13
A=M-D
D=M
@THIS
M=D
@3
D=A
@R13
A=M-D
D=M
@ARG
M=D
@4
D=A
@R13
A=M-D
D=M
@LCL
M=D
@R14
A=M
0;JMP
