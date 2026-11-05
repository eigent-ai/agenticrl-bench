#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <string>
#include <functional>
#include "algorithms.h"

std::vector<int> generate_random_vector(int size, int seed) {
    std::mt19937 gen(seed);
    std::uniform_int_distribution<int> dist(1, 1000000);
    std::vector<int> vec(size);
    for (int i = 0; i < size; i++) {
        vec[i] = dist(gen);
    }
    return vec;
}

double time_sort(std::function<void(std::vector<int>&)> sort_fn, std::vector<int> data) {
    auto start = std::chrono::system_clock::now();
    sort_fn(data);
    auto end = std::chrono::system_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count();
    double time_ms = static_cast<double>(duration) / 1000.0;
    return time_ms;
}

int main(int argc, char* argv[]) {
    int size = 10000;
    int runs = 5;

    for (int i = 1; i < argc; i++) {
        std::string arg = argv[i];
        if (arg == "--size" && i + 1 < argc) {
            size = std::stoi(argv[++i]);
        } else if (arg == "--runs" && i + 1 < argc) {
            runs = std::stoi(argv[++i]);
        }
    }

    struct AlgEntry {
        std::string name;
        std::function<void(std::vector<int>&)> fn;
    };

    std::vector<AlgEntry> algorithms = {
        {"bubble_sort", bubble_sort},
        {"insertion_sort", insertion_sort},
        {"selection_sort", selection_sort},
        {"std_sort", std_sort_wrapper}
    };

    std::cout << "algorithm\trun\ttime_ms" << std::endl;

    for (const auto& alg : algorithms) {
        for (int r = 1; r <= runs; r++) {
            auto data = generate_random_vector(size, r * 42);
            double t = time_sort(alg.fn, data);
            std::cout << alg.name << "\t" << r << "\t" << t << std::endl;
        }
    }

    return 0;
}
