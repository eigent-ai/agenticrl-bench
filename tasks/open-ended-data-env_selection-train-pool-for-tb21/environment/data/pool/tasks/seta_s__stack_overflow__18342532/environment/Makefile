CXX = g++
CXXFLAGS = -O2 -std=c++17
TARGET = datapipe
SRC = src/main.cpp src/datapipe.cpp

$(TARGET): $(SRC) src/datapipe.h
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET)
