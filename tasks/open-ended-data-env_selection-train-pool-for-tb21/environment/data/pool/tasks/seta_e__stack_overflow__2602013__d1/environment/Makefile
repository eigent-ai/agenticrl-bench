CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra
LDFLAGS = -lstdc++fs

SRCS = main.cpp file_reader.cpp normalizer.cpp
OBJS = $(SRCS:.cpp=.o)
TARGET = textmerge

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $<

clean:
	rm -f $(OBJS) $(TARGET)

.PHONY: all clean
