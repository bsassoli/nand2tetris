// pop from stack and put in local memory 2
// pop local 2 <=> addr = LCL + 2, SP--, *addr = *SP

// SETUP
@257
D=A
@0
M=D
@1001
D=A
@1
M=D
@2323
D=A
@257
M=D
// END SETUP
// BEGIN PROGRAM
@LCL
D=M
@2
D=D+A
@addr
M=D  // local 2
@SP
D=M-1 // SP--
M=D
@temp
A=D+1
D=M // Points to where we need to pop from
@addr
M=D
//END PROGRAM
(END)
    @END
    0;JMP