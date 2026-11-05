#include "text_search.h"

std::vector<size_t> TextSearch::find_all(const std::string& haystack,
                                         const std::string& needle) const {
    std::vector<size_t> positions;
    if (needle.empty()) return positions;

    size_t pos = haystack.find(needle);
    while (pos != static_cast<size_t>(static_cast<unsigned int>(-1))) {
        positions.push_back(pos);
        pos = haystack.find(needle, pos + 1);
    }
    return positions;
}
