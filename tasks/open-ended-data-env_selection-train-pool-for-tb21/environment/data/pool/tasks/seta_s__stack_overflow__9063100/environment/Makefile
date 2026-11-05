CC = gcc

.PHONY: debug release clean

debug: CFLAGS = -g -Wall -DDEBUG -DIS_DEBUG=1
debug: secpay

release: CFLAGS = -O2 -Wall -DDEBUG=0
release: secpay

secpay: main.c processor.c logger.c
	$(CC) $(CFLAGS) -o secpay main.c processor.c logger.c

clean:
	rm -f secpay /tmp/secpay.log
