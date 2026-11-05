CXX      = g++
CXXFLAGS = -Wall -Wextra -std=c++17
TARGET   = semf

all: $(TARGET)

$(TARGET): semf.cpp
	$(CXX) $(CXXFLAGS) -o $(TARGET) semf.cpp -lm

clean:
	rm -f $(TARGET)
