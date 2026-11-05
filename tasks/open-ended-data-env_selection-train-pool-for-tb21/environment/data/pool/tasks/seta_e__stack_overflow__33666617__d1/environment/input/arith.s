	.text
	.globl compute
	.type compute, @function
compute:
	pushq %rbp
	movq %rsp, %rbp
	movl $0, %eax  # clear accumulator
	movq $0, %rdx  # zero extend
	cmpl $0, %edi  # check if arg is zero
	je .Lskip
	addl %edi, %eax
	movl $1, %eax
	movl $42, %ecx
.Lskip:
	popq %rbp
	ret
	.size compute, .-compute
