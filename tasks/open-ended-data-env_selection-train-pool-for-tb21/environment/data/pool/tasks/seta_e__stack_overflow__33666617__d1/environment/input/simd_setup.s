	.text
	.globl simd_init
	.type simd_init, @function
simd_init:
	pushq %rbp
	movq %rsp, %rbp
	xorq %rax, %rax
	xorq %r10, %r10
	xorq %r11, %r11
	movq $0, %r8
	movq $0, %r9
	xorq %rcx, %rcx
	popq %rbp
	ret
	.size simd_init, .-simd_init
