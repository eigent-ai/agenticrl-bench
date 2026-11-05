	.text
	.globl check_values
	.type check_values, @function
check_values:
	pushq %rbp
	movq %rsp, %rbp
	test %al, %al
	jz .Lnull_byte
	test %eax, %eax
	je .Lzero_val
	testl %ecx, %ecx
	jne .Lnonzero
	testb %al, %al
	je .Lempty
	xorl %edx, %edx # default return
.Lnull_byte:
.Lzero_val:
.Lnonzero:
.Lempty:
	popq %rbp
	ret
	.size check_values, .-check_values
