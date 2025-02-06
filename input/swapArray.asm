# swap_array.asm program
# CS 64, Z.Matni
#
# IMPORTANT: READ, BUT DO NOT CHANGE ANY OF THE CODE IN THIS PROGRAM
#           THAT IS ALREADY THERE! ONLY ADD YOUR NEW CODE WHERE 
#           IT SAYS TODO SO, i.e. IN THE doSwap: AREA.

.data
# Data Area.  Note that while this is typically only
# For global immutable data, for SPIM, this also includes
# mutable data.        

incorrect:  .asciiz "---TEST FAILED---\n"
before:     .asciiz "Before:\n"
after:      .asciiz "After:\n"
comma:      .asciiz ", "
newline:    .asciiz "\n"
        
expectedMyArray:
        .word 17 29 20 27 22 25 24 23 26 21 28 19
myArray:
        .word 29 17 27 20 25 22 23 24 21 26 19 28

.text
# Print everything in the array (without use of a loop)
# Used as a function/sub-routine

printArray: # Again: DO NOT CHANGE THIS CODE BLOCK!
        la $t0, myArray

        li $v0, 1
        lw $a0, 0($t0)
        syscall
        li $v0, 4
        la $a0, comma
        syscall
        
        li $v0, 1
        lw $a0, 4($t0)
        syscall
        li $v0, 4
        la $a0, comma
        syscall

        li $v0, 1
        lw $a0, 8($t0)
        syscall
        li $v0, 4
        la $a0, comma
        syscall

        li $v0, 1
        lw $a0, 12($t0)
        syscall
        li $v0, 4
        la $a0, comma
        syscall

        li $v0, 1
        lw $a0, 16($t0)
        syscall
        li $v0, 4
        la $a0, comma
        syscall

        li $v0, 1
        lw $a0, 20($t0)
        syscall
        li $v0, 4
        la $a0, comma
        syscall

        li $v0, 1
        lw $a0, 24($t0)
        syscall
        li $v0, 4
        la $a0, comma
        syscall

        li $v0, 1
        lw $a0, 28($t0)
        syscall
        li $v0, 4
        la $a0, comma
        syscall

        li $v0, 1
        lw $a0, 32($t0)
        syscall
        li $v0, 4
        la $a0, comma
        syscall
		
	li $v0, 1
        lw $a0, 36($t0)
        syscall
        li $v0, 4
        la $a0, comma
        syscall

        li $v0, 1
        lw $a0, 40($t0)
        syscall
        li $v0, 4
        la $a0, comma
        syscall

        li $v0, 1
        lw $a0, 44($t0)
        syscall
        li $v0, 4
        la $a0, newline
        syscall

        jr $ra
        
checkArrays:  # Again: DO NOT CHANGE THIS CODE BLOCK!
        # $t0: p1
        # $t1: p2
        # $t2: limit
        
        la $t0, expectedMyArray
        la $t1, myArray
        addiu $t2, $t0, 44

checkArrays_loop:  # Again: DO NOT CHANGE THIS CODE BLOCK!
        slt $t3, $t0, $t2
        beq $t3, $zero, checkArrays_exit

        lw $t4, 0($t0)
        lw $t5, 0($t1)
        bne $t4, $t5, checkArrays_nonequal
        addiu $t0, $t0, 4
        addiu $t1, $t1, 4
        j checkArrays_loop
        
checkArrays_nonequal: # Again: DO NOT CHANGE THIS CODE BLOCK!
        li $v0, 0
        jr $ra
        
checkArrays_exit: # Again: DO NOT CHANGE THIS CODE BLOCK!
        li $v0, 1
        jr $ra
        
main:   # Again: DO NOT CHANGE THIS CODE BLOCK!
        # Print array "before"
        la $a0, before
        li $v0, 4
        syscall

        jal printArray
        
        # Do swap function 
        jal doSwap

        # Print array "after"
        la $a0, after
        li $v0, 4
        syscall
        
        jal printArray

        # Perform check on array
        jal checkArrays
        beq $v0, $zero, main_failed
        j main_exit
        
main_failed: # Again: DO NOT CHANGE THIS CODE BLOCK!
        la $a0, incorrect
        li $v0, 4
        syscall
        
main_exit:      
	li $v0, 10
    syscall

        
# COPYFROMHERE - DO ___NOT___ REMOVE THIS LINE

doSwap:
        # TODO: translate the following C/C++ code 
        # into MIPS assembly here.
        # Use only regs $v0-$v1, $t0-$t7, $a0-$a3.
        # You may assume nothing about their starting values.
        #
        #
        # unsigned int x = 0; 
        # unsigned int y = 1; 
        # while (x < 11) { 
        #    int temp = myArray[x]; 
        #    myArray[x] = myArray[y]; 
        #    myArray[y] = temp; 
        #    x+=2; 
        #    y+=2; 
        # }

        # TODO: fill in the assembly code here:

        # Set x and y (multiples of 4 because we're dealing with byte offsets)
        li $t0, 0
        li $t1, 4

        # Get starting address of array
        la $t4 myArray
loop:
        # Get addr of myArray[x] and myArray[y]
        addu $t5, $t4, $t0
        addu $t6, $t4, $t1

        # t7 = myArray[x], t8 = myArray[y]
        lw $t7, 0($t5)
        lw $t8, 0($t6)

        # Do swaps
        sw $t7, 0($t6)
        sw $t8, 0($t5)
        
        # Increment x and y
        addi $t0, 8
        addi $t1, 8

        # Keep going if x < 11
        slti $t2, $t1, 45 # 11*4 + 1
        bne $zero, $t2, loop


finished:
        # do ___NOT___ remove this last line
        jr $ra
