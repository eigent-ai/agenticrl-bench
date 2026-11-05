CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2
SRCS = src/main.cpp src/stream_reader.cpp src/mmap_reader.cpp
OBJS = $(SRCS:.cpp=.o)
TARGET = processor

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

src/%.o: src/%.cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $<

clean:
	rm -f $(OBJS) $(TARGET)

.PHONY: all clean
