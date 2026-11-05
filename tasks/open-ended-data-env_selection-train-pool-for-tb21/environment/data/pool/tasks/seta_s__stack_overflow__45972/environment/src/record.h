#ifndef RECORD_H
#define RECORD_H

#include <string>
#include <map>
#include <cstdint>
#include <limits>

// Maximum expected size for a single record payload
const uint32_t MAX_RECORD_SIZE = 128;

struct SensorStats {
    int count = 0;
    double sum = 0.0;
    uint64_t min_ts = std::numeric_limits<uint64_t>::max();
    uint64_t max_ts = 0;
};

using StatsMap = std::map<std::string, SensorStats>;

#endif
