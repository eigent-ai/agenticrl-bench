#ifndef LOGGER_H
#define LOGGER_H

#include <string>

class Logger {
public:
    void writeDebugLog(const std::string& message);
    void writeInfo(const std::string& message);
};

#endif
