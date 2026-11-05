CC      = gcc
CFLAGS  = -Wall -I/opt/libxml2/include
LDFLAGS = -L/opt/libxml2/lib -lxml2
TARGET  = write_xml
SRC     = write_xml.c

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC) $(LDFLAGS)

clean:
	rm -f $(TARGET) output.xml
