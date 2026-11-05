#pragma once
#include <cstdint>
#include <cstring>

const char MAGIC[4] = {'B', 'P', 'A', 'K'};

#pragma pack(push, 1)
struct Header {
    char magic[4];
    uint32_t record_count;
    uint64_t data_size;
};

struct Record {
    uint64_t id;
    double value;
    char label[32];
};
#pragma pack(pop)

const uint32_t CHUNK_SIZE = 64 * 1024 * 1024;
