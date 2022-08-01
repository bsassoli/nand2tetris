// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

//setup    
(LISTEN)
    @0
    D=A
    @i // counter
    M=D
    @8192
    D=A
    @k
    M=D
    @KBD
    D=M
    @FILL
    D;JNE
    @UNFILL
    0;JMP
    (FILL)
        // start filling
        @SCREEN
        D=A
        @i
        A=D+M
        M=-1
        @i
        D=M+1 //i++
        M=D
        @k
        D=M-1
        M=D
        @LISTEN
        D;JEQ
        @FILL
        0;JMP
    (UNFILL)
        // start filling
        @SCREEN
        D=A
        @i
        A=D+M
        M=0
        @i
        D=M+1 //i++
        M=D
        @k
        D=M-1
        M=D
        @LISTEN
        D;JEQ
        @UNFILL
        0;JMP