CC = gcc
CFLAGS = -O2 -Wall
SRC = src/main.c src/parser.c src/formatter.c
OBJ = $(SRC:.c=.o)
TARGET = dataproc

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^

src/%.o: src/%.c
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -f $(OBJ) $(TARGET)
