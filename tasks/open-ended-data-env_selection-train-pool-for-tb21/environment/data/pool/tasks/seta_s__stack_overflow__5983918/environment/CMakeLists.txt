cmake_minimum_required(VERSION 3.16)
project(mathutil C)

set(CMAKE_BUILD_TYPE Release)

add_executable(mathutil src/mathutil.c)
target_include_directories(mathutil PRIVATE src)
