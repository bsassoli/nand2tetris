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


// Start an infinite loop
(START)
// for (i = 0; i <= k=8191; i++ => arr[i]==-1)
// initialize i = 0
    @0
    D=A
    @i
    M=D
    // initialize k = 8191
    @8192
    D=A
    @k
    M=D
    // if i == k -> START
    // @i
    // D=M
    // @k
    // D=D-M
    // @START
    // D; JEQ
    // else LOOP
    // Check if keyboard is pressed
    @KBD
    D=M
    @FILL_LOOP
    D; JNE
    @UNFILL_LOOP
    0; JMP
    (FILL_LOOP)
        @SCREEN
        D=A
        @i
        A=D+M
        M=-1 // arr[i] = -1
        @i
        D=M
        D=D+1
        M=D // i++
        @i
        D=M
        @k
        D=D-M
        @START
        D; JEQ
        @FILL_LOOP
        0;JMP
    (UNFILL_LOOP)
        @SCREEN
        D=A
        @i
        A=D+M
        M=0 // arr[i] = 0
        @i
        D=M
        D=D+1
        M=D // i++
        @i
        D=M
        @k
        D=D-M
        @START
        D; JEQ
        @UNFILL_LOOP
        0;JMP
    