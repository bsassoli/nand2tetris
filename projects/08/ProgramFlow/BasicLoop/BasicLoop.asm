// init
@256
D=A
@SP
M=D
//C_PUSH constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
//C_POP local 0
@LCL
D=M
@0
D=D+A
@R13
M=D
@SP
M=M-1
D=M
@R15
M=D
A=M
D=M
M=D
@R13
A=M
M=D
(BasicLoop.asm.$LOOP_START)
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
//C_PUSH local 0
@LCL
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
//add
//add
@SP
M=M-1
A=M
D=M
A=A-1
M=D+M
//C_POP local 0
@LCL
D=M
@0
D=D+A
@R13
M=D
@SP
M=M-1
D=M
@R15
M=D
A=M
D=M
M=D
@R13
A=M
M=D
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
//C_PUSH constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
//sub
//sub
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D
//C_POP argument 0
@ARG
D=M
@0
D=D+A
@R13
M=D
@SP
M=M-1
D=M
@R15
M=D
A=M
D=M
M=D
@R13
A=M
M=D
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
@SP
AM=M-1
D=M
@BasicLoop.asm.$LOOP_START
D;JNE
//C_PUSH local 0
@LCL
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