#include <iostream>
#include <fstream>
#include <filesystem>
#include <vector>
#include <algorithm>
#include "file_reader.h"
#include "normalizer.h"

namespace fs = std::filesystem;

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <input_dir> <output_file>" << std::endl;
        return 1;
    }

    std::string inputDir = argv[1];
    std::string outputFile = argv[2];

    std::vector<std::string> txtFiles;
    for (const auto& entry : fs::directory_iterator(inputDir)) {
        if (entry.path().extension() == ".txt") {
            txtFiles.push_back(entry.path().filename().string());
        }
    }

    std::sort(txtFiles.begin(), txtFiles.end());

    std::string merged;
    for (const auto& filename : txtFiles) {
        std::string fullPath = inputDir + "/" + filename;
        std::string content = readFileToString(fullPath);
        merged += normalizeContent(filename, content);
    }

    std::ofstream ofs(outputFile);
    if (!ofs.is_open()) {
        std::cerr << "Error: could not open output file " << outputFile << std::endl;
        return 1;
    }
    ofs << merged;
    ofs.close();

    return 0;
}
