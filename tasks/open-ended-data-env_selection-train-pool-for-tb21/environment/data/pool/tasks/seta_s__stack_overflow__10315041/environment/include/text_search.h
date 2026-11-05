#pragma once
#include <string>
#include <vector>

class TextSearch {
public:
    std::vector<size_t> find_all(const std::string& haystack,
                                 const std::string& needle) const;
};
