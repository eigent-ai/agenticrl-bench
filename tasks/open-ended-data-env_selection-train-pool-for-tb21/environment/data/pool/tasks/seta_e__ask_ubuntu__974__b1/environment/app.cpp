#include <iostream>
#include <numeric>
#include <ranges>
#include <vector>

int main() {
    std::cout << "C++ Application Running!" << std::endl;
    std::cout << "GCC Version: " << __GNUC__ << "." << __GNUC_MINOR__ << "." << __GNUC_PATCHLEVEL__ << std::endl;

    // Use C++20 ranges feature (requires GCC 13 for full support)
    auto numbers = std::views::iota(1, 11);
    int result = 0;
    for (auto n : numbers) {
        result += n;
    }
    std::cout << "Sum of 1 to 10: " << result << std::endl;

    // Check if compiled with GCC 13
    if (__GNUC__ == 13) {
        std::cout << "SUCCESS: Compiled with GCC 13 as required!" << std::endl;
    } else {
        std::cout << "WARNING: Not compiled with GCC 13!" << std::endl;
    }

    return 0;
}
