// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.
// PSEUDOCODE
// Multiplication is just repeated addition
// ex.:  3 * 4 = 12 == 3 + 3 + 3 + 3
// Initialize sum to 0
@sum
M=0
// Store R0 as a
@R0
D=M
@a
M=D
@END
D;JLE // If a <= 0 -> END
// Store R1 as b
@R1
D=M
@b
M=D
@END
D;JLE // If B <= 0 -> END
// Else start loop
(LOOP)
    // add a to sum
    @sum
    D=M
    @a
    D=D+M
    @sum
    M=D
    // Decrease b by 1
    @b
    D=M
    D=D-1
    @b
    M=D // Store
    @END
    D;JLE // if b < 0 -> END
    @LOOP
    0; JMP // Else LOOP

(END)
// Store sum in R[2]
// then terminate
    @sum
    D=M // R2 = sum
    @R2
    M=D

(TERMINATE)
    @TERMINATE
    0; JMP
