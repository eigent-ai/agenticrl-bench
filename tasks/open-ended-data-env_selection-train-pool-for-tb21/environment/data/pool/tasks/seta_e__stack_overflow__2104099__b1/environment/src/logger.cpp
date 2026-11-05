#include "logger.h"
#include <iostream>

void Logger::writeDebugLog(const std::string& message) {
#ifdef DEBUG_MODE
    std::cout << "[DEBUG] " << message << std::endl;
#endif
}

void Logger::writeInfo(const std::string& message) {
    std::cout << "[INFO] " << message << std::endl;
}
