#include "scale.h"

static void fast_scale_double(double *d, int shift) {
    unsigned long long *bits = (unsigned long long *)d;
    *bits += ((unsigned long long)shift << 52);
}

double scale_float_reading(double raw, int scale_factor) {
    fast_scale_double(&raw, scale_factor);
    return raw;
}
