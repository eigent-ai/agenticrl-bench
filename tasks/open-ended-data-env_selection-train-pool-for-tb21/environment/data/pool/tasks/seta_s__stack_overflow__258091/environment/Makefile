CC = gcc
CFLAGS = -Wall -Wextra -O2

all: fi_index fi_search fi_cached

fi_index: src/indexer.c src/common.h
	$(CC) $(CFLAGS) -o fi_index src/indexer.c

fi_search: src/searcher.c src/common.h
	$(CC) $(CFLAGS) -o fi_search src/searcher.c

fi_cached: src/cache.c src/common.h
	$(CC) $(CFLAGS) -o fi_cached src/cache.c

clean:
	rm -f fi_index fi_search fi_cached *.idx

test: all
	./run_tests.sh

.PHONY: all clean test
