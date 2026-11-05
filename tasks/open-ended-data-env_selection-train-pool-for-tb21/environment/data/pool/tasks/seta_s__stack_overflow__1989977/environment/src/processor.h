#ifndef PROCESSOR_H
#define PROCESSOR_H

#include <string>
#include <vector>

struct ChunkTask {
    int chunk_id;
    std::vector<std::string> lines;
    std::string output_path;
    std::string header;
    int* total_counter;
};

void* process_chunk(void* arg);

#endif // PROCESSOR_H
