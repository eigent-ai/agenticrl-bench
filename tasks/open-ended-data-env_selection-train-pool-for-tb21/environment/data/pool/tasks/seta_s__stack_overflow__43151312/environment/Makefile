CC      = gcc
CFLAGS  = -Wall -I/opt/hdf5/include
LDFLAGS = -L/opt/hdf5/lib -lhdf5
TARGET  = write_dataset
SRC     = write_dataset.c

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC) $(LDFLAGS)

clean:
	rm -f $(TARGET) dset.h5
