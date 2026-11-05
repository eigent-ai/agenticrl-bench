CXX = g++
CXXFLAGS = -g -O0 -Wall
TARGET = rectools
SRCS = main.cpp factorial.cpp power.cpp fibonacci.cpp sum_tree.cpp
OBJS = $(SRCS:.cpp=.o)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

.PHONY: clean
