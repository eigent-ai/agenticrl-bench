CC = gcc
CFLAGS = -Wall -Wextra -DWIN32
TARGET = pathresolver

all: $(TARGET)

$(TARGET): pathresolver.c
	$(CC) $(CFLAGS) -o $(TARGET) pathresolver.c

clean:
	rm -f $(TARGET)

test-paths: $(TARGET)
	@echo "=== Path Resolution Tests ==="
	@echo -n "Saves path: "; ./$(TARGET) --saves
	@echo -n "Config path: "; ./$(TARGET) --config
	@echo -n "Exe dir: "; ./$(TARGET) --exe-dir
	@echo -n "State path: "; ./$(TARGET) --state
	@echo "=== Done ==="

.PHONY: all clean test-paths
