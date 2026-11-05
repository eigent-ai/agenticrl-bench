CC = gcc
CFLAGS = -Wall -O2

all: log_collector

log_collector: src/log_collector.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f log_collector
