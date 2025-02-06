# 1. SET UP THE ENVIRONMENT FOR THE EMULATOR
.text
# 2. WRITE THE ACTUAL INSTRUCTIONS
main:
li $t0, 5 # Assign 5 to “$t0”
li $t1, 7 # Assign 7 to “$t1”
add $t2, $t1, $t0 # Add “and put the result in “$t2”
# 3. SHOW THE RESULT BY EMULATING THE EXCHANGE BETWEEN CPU and OS.
# That is, print the result on the screen
# (equivalent to C++ instruction: cout << t2;)
li $v0, 1
move $a0, $t0
syscall
# 4. QUIT THE PROGRAM “PROPERLY”
li $v0, 10
syscall
