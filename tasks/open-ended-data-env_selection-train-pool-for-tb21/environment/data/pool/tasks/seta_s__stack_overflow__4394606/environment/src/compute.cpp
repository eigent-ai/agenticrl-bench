#include "compute.h"

long long slow_fibonacci(int n) {
    if (n <= 1) return n;
    return slow_fibonacci(n - 1) + slow_fibonacci(n - 2);
}

double matrix_trace(int size) {
    double sum = 0.0;
    for (int i = 0; i < size; i++) {
        sum += (double)slow_fibonacci(28 + (i % 5));
    }
    return sum;
}
