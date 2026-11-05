#include <iostream>
#include "common.h"

long collatz_length(long n) {
    long count = 0;
    while (n != 1) {
        if (n % 2 == 0)
            n = n / 2;
        else
            n = 3 * n + 1;
        count++;
    }
    return count;
}

int main() {
    auto start = bench::timer_start();
    long max_start = 1;
    long max_length = 0;
    for (long i = 999999; i > 0; --i) {
        long len = collatz_length(i);
        if (len >= max_length) {
            max_length = len;
            max_start = i;
        }
    }
    double elapsed = bench::timer_elapsed_ms(start);
    std::cout << "Longest chain starting number: " << max_start << std::endl;
    std::cout << "Chain length: " << max_length << std::endl;
    std::cout << "Time: " << elapsed << " ms" << std::endl;
    return 0;
}
