#include "pipeline.h"
#include <sstream>
#include <cstring>

size_t DataPipeline::find_next_record(size_t start) {
    int pos = static_cast<int>(start);

    while (pos < (int)g_data_length && g_data_buffer[pos] != '\n')
        pos++;
    pos++;

    while (pos < (int)g_data_length && g_data_buffer[pos] == '\n')
        pos++;

    if (pos >= (int)g_data_length) return std::string::npos;
    return static_cast<size_t>(pos);
}

int DataPipeline::parse_record(size_t pos, size_t end) {
    std::string line = g_data_buffer.substr(pos, end - pos);
    std::istringstream ss(line);
    std::string field;
    int count = 0;

    while (std::getline(ss, field, ',')) {
        if (count >= 64) break;
        try {
            if (!field.empty() && (field[0] == '-' || field[0] == '+' || field[0] == '.' ||
                (field[0] >= '0' && field[0] <= '9'))) {
                g_record_buffer[count] = std::stod(field);
            } else {
                g_record_buffer[count] = 0.0;
            }
        } catch (...) {
            g_record_buffer[count] = 0.0;
        }
        count++;
    }
    return count;
}
