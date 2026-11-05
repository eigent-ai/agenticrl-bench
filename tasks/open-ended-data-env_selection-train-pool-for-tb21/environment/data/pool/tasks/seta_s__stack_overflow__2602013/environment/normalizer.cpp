#include "normalizer.h"

std::string normalizeContent(const std::string& filename, const std::string& content) {
    std::string result = "=== " + filename + " ===\n";
    result += content;
    if (!content.empty() && content.back() != '\n') {
        result += "\n";
    }
    return result;
}
