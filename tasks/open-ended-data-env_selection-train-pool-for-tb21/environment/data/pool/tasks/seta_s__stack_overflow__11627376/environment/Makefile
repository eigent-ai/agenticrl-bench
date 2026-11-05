CC = gcc
CFLAGS = -Wall -Wextra -O2
HDF5_CFLAGS = $(shell pkg-config --cflags hdf5)
HDF5_LIBS = $(shell pkg-config --libs hdf5)

all: process_data

process_data: process_data.c
	$(CC) $(CFLAGS) $(HDF5_CFLAGS) -o $@ $< $(HDF5_LIBS)

clean:
	rm -f process_data

.PHONY: all clean
