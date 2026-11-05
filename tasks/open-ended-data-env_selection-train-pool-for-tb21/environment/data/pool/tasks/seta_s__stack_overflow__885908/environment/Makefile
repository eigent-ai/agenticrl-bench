CC = gcc
CFLAGS = -O2
OBJDIR = output
SRC = src/variants.c
OBJ = $(OBJDIR)/variants.o
ASM = $(OBJDIR)/variants.asm
DUMP = $(OBJDIR)/variants.objdump

# Debug: use unoptimized builds for local testing
CFLAGS = -O0

.PHONY: all clean report

all: $(DUMP)

$(OBJDIR):
	mkdir -p $(OBJDIR)

$(OBJ): $(SRC) | $(OBJDIR)
	$(CC) $(CFLAGS) -c -o $@ $<

$(ASM): $(SRC) | $(OBJDIR)
	$(CC) $(CFLAGS) -S -o $@ $<

$(DUMP): $(OBJ) | $(OBJDIR)
	objdump -d $< > $@

report: $(DUMP) $(ASM)
	python3 scripts/analyze.py

clean:
	rm -rf $(OBJDIR)
