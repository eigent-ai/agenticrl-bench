#include "string_pool.h"
#include <algorithm>
#include <limits>

void StringPool::add(const char* s, size_t len) {
    pool_.emplace_back(s, len);
}

const CompactString& StringPool::get(size_t index) const {
    return pool_.at(index);
}

size_t StringPool::size() const {
    return pool_.size();
}

int StringPool::find(const char* s) const {
    CompactString target(s);
    for (size_t i = 0; i < pool_.size(); ++i) {
        if (pool_[i] == target) {
            return static_cast<int>(i);
        }
    }
    return -1;
}

size_t StringPool::unique_count() const {
    std::vector<CompactString> sorted(pool_.begin(), pool_.end());
    std::sort(sorted.begin(), sorted.end());
    auto last = std::unique(sorted.begin(), sorted.end());
    return static_cast<size_t>(last - sorted.begin());
}

size_t StringPool::longest() const {
    size_t max_len = 0;
    for (const auto& s : pool_) {
        if (s.size() > max_len) max_len = s.size();
    }
    return max_len;
}

size_t StringPool::shortest_nonempty() const {
    size_t min_len = std::numeric_limits<size_t>::max();
    for (const auto& s : pool_) {
        if (!s.empty() && s.size() < min_len) {
            min_len = s.size();
        }
    }
    return min_len == std::numeric_limits<size_t>::max() ? 0 : min_len;
}
