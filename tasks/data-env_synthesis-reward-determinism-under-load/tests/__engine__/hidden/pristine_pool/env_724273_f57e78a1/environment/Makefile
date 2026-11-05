CC     = gcc
CFLAGS = -Wall -Werror -std=c99
LDFLAGS = -lX1l

TARGET = find-cursor
SOURCE = find-cursor.c

all: $(TARGET)

$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) $(SOURCE) -o $(TARGET) $(LDFLAGS)

clean:
	rm -f $(TARGET)

test: $(TARGET)
	bash run_tests.sh
