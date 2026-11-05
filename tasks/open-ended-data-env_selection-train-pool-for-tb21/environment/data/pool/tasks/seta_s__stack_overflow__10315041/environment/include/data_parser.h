#pragma once
#include <string>
#include <vector>

class DataParser {
public:
    std::vector<double> parse_fields(const std::string& line,
                                     char delimiter) const;
};
