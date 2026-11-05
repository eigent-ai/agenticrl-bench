CC = gcc
CFLAGS = -Wall -Werror -Wunused-result -O2 -Iinclude
LDFLAGS =

SRC = src/main.c src/search.c src/classifier.c src/lookup.c
OBJ = $(SRC:.c=.o)
TARGET = classifier

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(OBJ) -o $(TARGET) $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

test: $(TARGET)
	@echo "Running correctness tests..."
	./$(TARGET) --file data/test_input.dat > /tmp/test_actual.dat
	diff data/expected_output.dat /tmp/test_actual.dat
	@echo "All correctness tests passed!"

clean:
	rm -f $(OBJ) $(TARGET)

.PHONY: all test clean
