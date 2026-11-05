CC = gcc
CFLAGS = -Wall -Werror -Wextra -I include/ -DFEATURE_LOG=1
SRCDIR = src
BUILDDIR = build
SOURCES = $(SRCDIR)/main.c $(SRCDIR)/platform.c $(SRCDIR)/logger.c $(SRCDIR)/utils.c
OBJECTS = $(BUILDDIR)/main.o $(BUILDDIR)/platform.o $(BUILDDIR)/logger.o $(BUILDDIR)/utils.o
TARGET = $(BUILDDIR)/app

all: $(TARGET)

$(BUILDDIR):
	mkdir -p $(BUILDDIR)

$(BUILDDIR)/%.o: $(SRCDIR)/%.c | $(BUILDDIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) $^ -o $@

clean:
	rm -rf $(BUILDDIR)

.PHONY: all clean
