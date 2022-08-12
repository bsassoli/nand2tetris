// bootstrap code
@256
D=A
@SP
M=D
// push return address
@Sys.initRET0
D=A
@SP
A=M
M=D
@SP
M=M+1
// store LCL ARG THIS THAT
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// reposition LCL
@SP
D=M
@LCL
M=D
// reposition ARG (n=number of args)
@5
D=D-A
@ARG
M=D
// function call preparation done, ready to jump
@Sys.init
0;JMP
// create the returning point
(Sys.initRET0)
// //// Processing Main.vm
// File namespace changes to Main
// Translate command: function Main.fibonacci 0
// define function Main.fibonacci
(Main.fibonacci)
// namespace changes to Main.fibonacci
// Translate command: push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: lt                     
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@BOOL_START_0
D;JLT
@SP
A=M
M=0
@BOOL_END_0
0;JMP
(BOOL_START_0)
@SP
A=M
M=-1
(BOOL_END_0)
@SP
M=M+1
// Translate command: if-goto IF_TRUE
@SP
M=M-1
@SP
A=M
D=M
@Main.fibonacci:IF_TRUE
D;JNE
// Translate command: goto IF_FALSE
@Main.fibonacci:IF_FALSE
0;JMP
// Translate command: label IF_TRUE          
(Main.fibonacci:IF_TRUE)
// Translate command: push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Translate command: return
@LCL
D=M
@R13
M=D
// RET = *(FRAME-5)
@R13
D=M
@5
D=D-A
A=D
D=M
@R14
M=D
// *ARG = pop
@SP
M=M-1
@SP
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R13
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@R13
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@R13
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@R13
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
// goto RET
@R14
A=M
0;JMP
// Translate command: label IF_FALSE         
(Main.fibonacci:IF_FALSE)
// Translate command: push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: sub
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
M=M+1
// Translate command: call Main.fibonacci 1  
// push return address
@Main.fibonacciRET1
D=A
@SP
A=M
M=D
@SP
M=M+1
// store LCL ARG THIS THAT
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// reposition LCL
@SP
D=M
@LCL
M=D
// reposition ARG (n=number of args)
@6
D=D-A
@ARG
M=D
// function call preparation done, ready to jump
@Main.fibonacci
0;JMP
// create the returning point
(Main.fibonacciRET1)
// Translate command: push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Translate command: push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: sub
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
M=M+1
// Translate command: call Main.fibonacci 1  
// push return address
@Main.fibonacciRET2
D=A
@SP
A=M
M=D
@SP
M=M+1
// store LCL ARG THIS THAT
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// reposition LCL
@SP
D=M
@LCL
M=D
// reposition ARG (n=number of args)
@6
D=D-A
@ARG
M=D
// function call preparation done, ready to jump
@Main.fibonacci
0;JMP
// create the returning point
(Main.fibonacciRET2)
// Translate command: add                    
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M+D
@SP
M=M+1
// Translate command: return
@LCL
D=M
@R13
M=D
// RET = *(FRAME-5)
@R13
D=M
@5
D=D-A
A=D
D=M
@R14
M=D
// *ARG = pop
@SP
M=M-1
@SP
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R13
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@R13
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@R13
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@R13
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
// goto RET
@R14
A=M
0;JMP
// //// Processing Sys.vm
// File namespace changes to Sys
// Translate command: function Sys.init 0
// define function Sys.init
(Sys.init)
// namespace changes to Sys.init
// Translate command: push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
// Translate command: call Main.fibonacci 1   
// push return address
@Main.fibonacciRET3
D=A
@SP
A=M
M=D
@SP
M=M+1
// store LCL ARG THIS THAT
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// reposition LCL
@SP
D=M
@LCL
M=D
// reposition ARG (n=number of args)
@6
D=D-A
@ARG
M=D
// function call preparation done, ready to jump
@Main.fibonacci
0;JMP
// create the returning point
(Main.fibonacciRET3)
// Translate command: label WHILE
(Sys.init:WHILE)
// Translate command: goto WHILE              
@Sys.init:WHILE
0;JMP