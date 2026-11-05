cmake_minimum_required(VERSION 3.10)
project(vidstats)

set(CMAKE_CXX_STANDARD 17)

find_package(OpenCV 3.0 REQUIRED)

add_executable(vidstats src/main.cpp)

target_link_libraries(video_stats ${OpenCV_LIBS})
