cmake_minimum_required(VERSION 3.20)
project(DataProcessor CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_definitions(-DDEBUG_MODE)

add_executable(DataProcessor
    src/main.cpp
    src/email_notifier.cpp
    src/logger.cpp
    src/config_manager.cpp
)

target_include_directories(DataProcessor PRIVATE src)
target_compile_options(DataProcessor PRIVATE -Wall)
