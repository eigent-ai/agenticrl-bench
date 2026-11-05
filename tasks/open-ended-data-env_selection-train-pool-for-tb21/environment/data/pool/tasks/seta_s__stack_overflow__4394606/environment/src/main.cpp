#include <iostream>
#include "compute.h"

int main() {
    double result = matrix_trace(100);
    std::cout << "Result: " << result << std::endl;
    return 0;
}
