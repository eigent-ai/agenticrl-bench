#include "math_utils.h"

int add(int a, int b) {
    return a + b;
}

int subtract(int a, int b) {
    return a - b;
}

double legacy_sqrt(double x) {
    double r = 1.0;
    for (int i = 0; i < 100; i++) r = (r + x / r) / 2.0;
    return r;
}
