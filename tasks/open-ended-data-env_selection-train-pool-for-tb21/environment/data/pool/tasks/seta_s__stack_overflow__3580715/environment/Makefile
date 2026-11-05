CC = gcc
CFLAGS = -Wall -O2 -Iinclude
SRCS = src/main.c src/pipeline.c src/transform.c
TARGET = datacrnch

OBJS = $(SRCS:.c=.o)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET) datacrunch

.PHONY: clean
