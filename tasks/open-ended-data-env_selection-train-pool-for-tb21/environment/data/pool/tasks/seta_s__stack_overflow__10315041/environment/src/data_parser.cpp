#include "data_parser.h"
#include <sstream>

std::vector<double> DataParser::parse_fields(const std::string& line,
                                             char delimiter) const {
    std::vector<double> result;
    std::istringstream line_stream(line);
    std::string token;
    std::istringstream converter;

    while (std::getline(line_stream, token, delimiter)) {
        double val = 0.0;
        converter.str(token);
        converter.seekg(0);
        converter >> val;
        result.push_back(val);
    }
    return result;
}
