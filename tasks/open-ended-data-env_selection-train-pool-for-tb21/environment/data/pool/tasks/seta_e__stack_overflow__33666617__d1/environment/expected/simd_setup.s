	.text
	.globl simd_init
	.type simd_init, @function
simd_init:
	pushq %rbp
	movq %rsp, %rbp
	xorl %eax, %eax
	xorl %r10d, %r10d
	xorl %r11d, %r11d
	xorl %r8d, %r8d
	xorl %r9d, %r9d
	xorl %ecx, %ecx
	popq %rbp
	ret
	.size simd_init, .-simd_init
