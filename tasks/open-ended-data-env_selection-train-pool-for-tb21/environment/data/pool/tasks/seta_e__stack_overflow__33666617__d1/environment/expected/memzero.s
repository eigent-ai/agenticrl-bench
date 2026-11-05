	.text
	.globl memzero_region
	.type memzero_region, @function
memzero_region:
	pushq %rbp
	movq %rsp, %rbp
	xorl %ecx, %ecx # loop counter
	movl $0, (%rdi)
	movl $0, 8(%rdi)
	movl $0, 16(%rdi)
	movq $0, (%rsi)
.Lloop:
	cmpl %edx, %ecx
	jge .Ldone
	movl $0, (%rdi,%rcx,4)
	incl %ecx
	jmp .Lloop
.Ldone:
	popq %rbp
	ret
	.size memzero_region, .-memzero_region
