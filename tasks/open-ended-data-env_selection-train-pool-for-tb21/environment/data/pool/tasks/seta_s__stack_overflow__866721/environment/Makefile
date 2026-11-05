CC      = gcc
CFLAGS  = -g -O0
BINARY  = mathutil

all: $(BINARY)

$(BINARY): src/mathutil.c
	$(CC) $(CFLAGS) -o $(BINARY) src/mathutil.c

clean:
	rm -f $(BINARY)
	rm -rf .debug
