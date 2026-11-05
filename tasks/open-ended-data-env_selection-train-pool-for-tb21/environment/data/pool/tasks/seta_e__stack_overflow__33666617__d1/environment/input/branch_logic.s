	.text
	.globl check_values
	.type check_values, @function
check_values:
	pushq %rbp
	movq %rsp, %rbp
	or %al, %al
	jz .Lnull_byte
	or %eax, %eax
	je .Lzero_val
	cmpl $0, %ecx
	jne .Lnonzero
	cmpb $0, %al
	je .Lempty
	movl $0, %edx  # default return
.Lnull_byte:
.Lzero_val:
.Lnonzero:
.Lempty:
	popq %rbp
	ret
	.size check_values, .-check_values
