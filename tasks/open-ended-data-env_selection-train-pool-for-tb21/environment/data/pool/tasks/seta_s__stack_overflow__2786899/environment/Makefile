CC = gcc
CFLAGS = -O2 -std=c11 -Wall -Werror

all: test_sort pipeline

test_sort: test_sort.c microsort.h microsort.c
	$(CC) $(CFLAGS) -o test_sort test_sort.c microsort.c

pipeline: pipeline.c microsort.h microsort.c
	$(CC) $(CFLAGS) -o pipeline pipeline.c microsort.c

clean:
	rm -f test_sort pipeline data/output.txt
