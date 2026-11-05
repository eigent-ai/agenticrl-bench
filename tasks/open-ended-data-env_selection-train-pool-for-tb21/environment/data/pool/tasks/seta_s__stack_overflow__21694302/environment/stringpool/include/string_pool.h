#pragma once

#include "compact_string.h"
#include <vector>
#include <cstddef>

class StringPool {
public:
    StringPool() = default;

    void add(const char* s, size_t len);
    const CompactString& get(size_t index) const;
    size_t size() const;
    int find(const char* s) const;

    size_t unique_count() const;
    size_t longest() const;
    size_t shortest_nonempty() const;

private:
    std::vector<CompactString> pool_;
};
