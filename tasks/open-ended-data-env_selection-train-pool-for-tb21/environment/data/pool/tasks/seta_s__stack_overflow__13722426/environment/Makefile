CXX = g++-13
CXXFLAGS = -O2 -std=c++17 -Wall -Werror

all: main benchmark

main: main.cpp pipeline.hpp
	$(CXX) $(CXXFLAGS) -o main main.cpp

benchmark: benchmark.cpp
	$(CXX) $(CXXFLAGS) -o benchmark benchmark.cpp

test: all
	@echo "Running main..."
	./main
	@echo "Running benchmark..."
	./benchmark
	@echo "All tests completed."

clean:
	rm -f main benchmark
