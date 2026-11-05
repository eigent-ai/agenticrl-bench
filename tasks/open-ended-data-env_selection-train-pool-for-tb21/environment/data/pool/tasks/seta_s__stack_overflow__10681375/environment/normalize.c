#include "normalize.h"

static long long halve_value(long long x) {
    return x >> 1;
}

long long normalize_int_reading(long long raw, int scale_factor) {
    long long result = raw;
    for (int i = 0; i < scale_factor; i++) {
        result = halve_value(result);
    }
    return result;
}
