CC = gcc
CFLAGS = -Wall -O2
PREFIX = /usr

all: countwords

countwords: countwords.c
	$(CC) $(CFLAGS) -o countwords countwords.c

install: countwords
	install -d $(PREFIX)/bin
	install -m 755 countwords $(PREFIX)/bin/countwords

clean:
	rm -f countwords
