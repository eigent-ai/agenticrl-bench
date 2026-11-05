CC = gcc
CFLAGS = -Wall -Wextra -g -fsanitize=address -I include
LDFLAGS = -fsanitize=address

SRC = src/cowstring.c
TEST_SRC = tests/test_cowstring.c
MAIN_SRC = src/main.c

all: cowstring_demo

cowstring_demo: $(SRC) $(MAIN_SRC)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

test: test_runner
	./test_runner

test_runner: $(SRC) $(TEST_SRC)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

clean:
	rm -f cowstring_demo test_runner

.PHONY: all test clean
