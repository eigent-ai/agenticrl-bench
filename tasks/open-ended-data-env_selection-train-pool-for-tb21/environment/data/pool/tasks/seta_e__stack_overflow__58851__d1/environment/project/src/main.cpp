#include "pipeline.h"
#include <iostream>

double g_record_buffer[64];
std::string g_data_buffer;
size_t g_data_length = 0;

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " input.csv output.csv" << std::endl;
        return 1;
    }
    return DataPipeline::process_batch(argv[1], argv[2]);
}
