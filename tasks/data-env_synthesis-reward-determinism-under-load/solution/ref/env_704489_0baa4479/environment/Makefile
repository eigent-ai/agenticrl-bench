all: p14_asm p14_cpp

p14_asm: p14.asm
	nasm -felf64 p14.asm -o p14.o && gcc -no-pie p14.o -o p14_asm

p14_cpp: p14.cpp
	g++ -O3 p14.cpp -o p14_cpp

clean:
	rm -f p14.o p14_asm p14_cpp
