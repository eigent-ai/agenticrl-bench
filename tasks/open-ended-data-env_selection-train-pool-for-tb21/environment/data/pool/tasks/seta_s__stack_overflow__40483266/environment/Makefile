CXX = g++
CXXFLAGS = -Wall -Werror -O2
SRCS = src/main.cpp src/router.cpp src/stats.cpp src/utils.cpp
OBJS = $(SRCS:.cpp=.o)
TARGET = router

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

.PHONY: all clean
