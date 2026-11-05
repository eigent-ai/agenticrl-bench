#include "file_reader.h"
#include <fstream>
#include <iterator>
#include <string>

std::string readFileToString(const std::string& path) {
    std::ifstream ifs(path);
    if (!ifs.is_open()) {
        return "";
    }

    ifs.seekg(0, std::ios::end);
    std::streamsize size = ifs.tellg();
    ifs.seekg(0, std::ios::beg);

    std::string content;
    content.reserve(static_cast<size_t>(size));
    content.assign(std::istreambuf_iterator<char>(ifs),
                   std::istreambuf_iterator<char>());

    return content;
}
