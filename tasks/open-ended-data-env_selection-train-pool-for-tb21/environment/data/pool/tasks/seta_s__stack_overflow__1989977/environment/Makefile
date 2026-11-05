CXX = g++
CXXFLAGS = -std=c++17 -O2 -Wall
LDFLAGS = -lthread

SRCDIR = src
SOURCES = $(SRCDIR)/main.cpp $(SRCDIR)/buffer.cpp $(SRCDIR)/processor.cpp
TARGET = chunkproc

all: $(TARGET)

$(TARGET): $(SOURCES)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

clean:
	rm -f $(TARGET)

.PHONY: all clean
