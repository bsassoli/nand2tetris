// computes R2 = R0 // R1
// assumes a, b posiive
// halts if b == 0

// Pseudocode
// Rembember that division is repeated subtraction:

// Initialize a == R0
@R0
D=M
@a
M=D
@a
D=M
@END
D;JEQ // If a == 0 -> set R2 to 0 then END

// Initialize b == R1
@R1
D=M
@b
M=D
@b
D=M
@NUM_IS_ZERO
D;JEQ // If a == 0 -> END (undefined)
// Else:
// Initialize counter i = 0
@0
D=A
@i
M=D
(LOOP)
    // a = a - b
    @b
    D=M
    @a
    M=M-D
    // if (a <= 0):
        //  R2 = i
        // -> END
    // i++
    D=M
    @END
    D;JLT
    // else i++
    @i
    D=M
    M=D+1
    @LOOP
    0;JMP

(NUM_IS_ZERO)
    @0
    D=A
    @R2
    M=D
    @TERMINATE
    0,JMP

(END)
    @i
    D=M
    @R2
    M=D
    @TERMINATE
    (TERMINATE)
    0; JMP


