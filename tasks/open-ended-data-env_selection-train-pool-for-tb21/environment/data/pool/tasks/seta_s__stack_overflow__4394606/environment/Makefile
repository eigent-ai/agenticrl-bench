CXX      = g++
CXXFLAGS = -O0 -Wall
TARGET   = profiler_demo
SRCS     = src/main.cpp src/compute.cpp

$(TARGET): $(SRCS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRCS)

clean:
	rm -f $(TARGET) gmon.out gprof_report.txt profile.dot

.PHONY: clean
