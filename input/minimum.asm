# minimum.asm program
# CS 64, Z.Matni
#
# Get 3 integer inputs from the user (std.in)
# Reveal the minimum value
# See assignment description for details

.data
	prompt: .asciiz "Enter the next number:\n"
    newline: .asciiz "\n"
	minimum: .asciiz "Minimum: "

.text
main:
	# Get a
	li $v0, 4
	la $a0, prompt
	syscall
	li $v0, 5
	syscall
	move $t0, $v0

	# Get b
	li $v0, 4
	la $a0, prompt
	syscall
	li $v0, 5
	syscall
	move $t1, $v0

	# Get c
	li $v0, 4
	la $a0, prompt
	syscall
	li $v0, 5
	syscall
	move $t2, $v0

	# Print "Minimum: "
	li $v0, 4
	la $a0, minimum
	syscall

	# $t4 is true if a < b
	slt $t4, $t0, $t1
	
	# $t5 is true if a < c
	slt $t5, $t0, $t2

	# $t6 is true if b < c
	slt $t6, $t1, $t2

	# If $t4 and $t5, then print A
	and $t9, $t4, $t5
	bne $zero, $t9, printA

	# If not $t4 and $t6, then print B
	nor $t7, $t4, $zero
	and $t9, $t7, $t6
	bne $zero, $t9, printB

	# If not $t5 and not $t6, then print C
	nor $t7, $t5, $zero
	nor $t8, $t6, $zero
	and $t9, $t7, $t8
	bne $zero, $t9, printC
	
	# Logic error!
	j exit


printA:
	li $v0, 1
	move $a0, $t0
	syscall
	j exit

printB:
	li $v0, 1
	move $a0, $t1
	syscall
	j exit

printC:
	li $v0, 1
	move $a0, $t2
	syscall
	j exit

exit:
	li $v0, 4
	la $a0, newline
	syscall

	li $v0, 10
	syscall