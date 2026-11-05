CC = gcc
CFLAGS = -Wall -O2
TARGET = dataproc

all: $(TARGET)

$(TARGET): dataproc.c
	$(CC) $(CFLAGS) -o $(TARGET) dataproc.c

clean:
	rm -f $(TARGET)

.PHONY: all clean
