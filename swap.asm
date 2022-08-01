// Swaps R0 and R1
// temp = a; a = b ; b = temp  



@R0
D=M
@temp
M=D
D=M  // temp = R0
@R1
D=M
@R0
M=D // R0 = R1
@temp
D=M
@R1
M=D // R1 = temp
(END)
    @END
    0;JMP