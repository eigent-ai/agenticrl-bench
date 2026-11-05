CXX      = g++
CXXFLAGS = -std=c++17 -Wall -Wextra
TARGET   = analyzer
SRC      = src/analyzer.cpp

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET) output.txt
