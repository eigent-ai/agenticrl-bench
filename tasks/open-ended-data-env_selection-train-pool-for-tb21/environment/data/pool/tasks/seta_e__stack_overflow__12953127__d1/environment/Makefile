CXX = g++
CXXFLAGS = -std=c++14 -fno-elide-constructors -Wall -Wextra -g -Iinclude

SRCS = src/main.cpp src/factory.cpp
OBJS = $(SRCS:.cpp=.o)
TARGET = rvo_bench

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

src/%.o: src/%.cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $<

test: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(OBJS) $(TARGET)

print-cxxflags:
	@echo $(CXXFLAGS)

.PHONY: all test clean print-cxxflags
