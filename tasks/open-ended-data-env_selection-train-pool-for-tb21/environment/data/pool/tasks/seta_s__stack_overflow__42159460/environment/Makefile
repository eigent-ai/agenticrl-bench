CC      = gcc
CFLAGS  = -O2 -march=native

LIB_SRC = libsig.c
LIB_OBJ = libsig.o
LIB_SO  = libsig.so
ASM_OUT = libsig.s

all: $(LIB_SO) main

$(LIB_SO): $(LIB_SRC)
	$(CC) $(CFLAGS) -shared -fPIC -o $@ $<

$(LIB_OBJ): $(LIB_SRC)
	$(CC) $(CFLAGS) -c -o $@ $<

main: main.c $(LIB_OBJ)
	$(CC) $(CFLAGS) -o $@ $< $(LIB_OBJ)

asm:
	$(CC) $(CFLAGS) -S $(LIB_SRC) -o $(ASM_OUT)

clean:
	rm -f $(LIB_OBJ) $(LIB_SO) $(ASM_OUT) main
