#include <iostream>
#include <string>
#include <cstring>
#include <iomanip>
#include "record.h"
#include "stream_reader.h"
#include "mmap_reader.h"

void print_stats(const StatsMap& stats) {
    for (const auto& [id, s] : stats) {
        std::cout << id << ","
                  << s.count << ","
                  << std::fixed << std::setprecision(2) << s.sum << ","
                  << s.min_ts << ","
                  << s.max_ts << std::endl;
    }
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0] << " --mode=stream|mmap <datafile>" << std::endl;
        return 1;
    }

    std::string mode_arg = argv[1];
    std::string filename = argv[2];

    std::string mode;
    if (mode_arg.substr(0, 7) == "--mode=") {
        mode = mode_arg.substr(7);
    } else {
        std::cerr << "Error: first argument must be --mode=stream or --mode=mmap" << std::endl;
        return 1;
    }

    StatsMap stats;
    if (mode == "stream") {
        stats = read_stream(filename);
    } else if (mode == "mmap") {
        stats = read_mmap(filename);
    } else {
        std::cerr << "Error: unknown mode '" << mode << "'" << std::endl;
        return 1;
    }

    print_stats(stats);
    return 0;
}
