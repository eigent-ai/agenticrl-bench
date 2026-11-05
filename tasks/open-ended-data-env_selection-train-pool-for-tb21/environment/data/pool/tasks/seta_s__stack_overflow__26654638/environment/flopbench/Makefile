CC      = gcc
CFLAGS  = -Wall -O0 -fno-tree-vectorize -ffloat-store
TARGET  = flopbench
SRC     = bench.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC) -lm

clean:
	rm -f $(TARGET)
