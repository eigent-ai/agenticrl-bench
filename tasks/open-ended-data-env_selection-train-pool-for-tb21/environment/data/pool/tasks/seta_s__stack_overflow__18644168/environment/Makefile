CC = gcc
CFLAGS = -Wall -Wextra
LDFLAGS =

SRCS = src/main.c src/stats.c src/anomaly.c src/report.c
OBJS = $(SRCS:.c=.o)
TARGET = numcrunch

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) -o $@ $^ $(LDFLAGS)

src/%.o: src/%.c
	$(CC) $(CFLAGS) -Iinclude -c -o $@ $<

clean:
	rm -f $(OBJS) $(TARGET) output.txt

.PHONY: all clean
