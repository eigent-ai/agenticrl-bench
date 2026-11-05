CC      = gcc
CFLAGS  = -Wall -Wextra -Werror -std=c11
TARGET  = test_bitutils

all: $(TARGET)

$(TARGET): test_bitutils.c bitutils.c bitutils.h
	$(CC) $(CFLAGS) -o $(TARGET) test_bitutils.c bitutils.c

test: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET)
