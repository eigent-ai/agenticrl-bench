#pragma once
#include <string>
#include <cstddef>

extern double g_record_buffer[64];
extern std::string g_data_buffer;
extern size_t g_data_length;

namespace DataPipeline {
    size_t find_next_record(size_t start);
    int parse_record(size_t pos, size_t end);
    void transform_record(int field_count);
    void apply_filter(int field_count);
    int process_batch(const std::string& input_file, const std::string& output_file);
}
