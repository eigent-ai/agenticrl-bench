#include <omp.h>
#include <iostream>
#include <vector>
#include "numlib.h"

int main() {
    const int N = 1000;
    std::vector<int> data(N);

    #pragma omp parallel for
    for (int i = 0; i < N; i++) {
        data[i] = i + 1;
    }

    #pragma omp parallel
    {
        #pragma omp single
        {
            std::cout << "Running with " << omp_get_num_threads()
                      << " thread(s)" << std::endl;
        }
    }

    long long result = compute_checksum(data.data(), N);
    std::cout << "Checksum: " << result << std::endl;
    return 0;
}
