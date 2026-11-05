CXX      = g++
CXXFLAGS = -std=c++14 -O2 -Wall -Wextra -I include
TARGET   = classifier
SRCS     = src/main.cpp src/classify.cpp src/filter.cpp
OBJS     = $(SRCS:.cpp=.o)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $<

clean:
	rm -f $(OBJS) $(TARGET) data/results.txt
