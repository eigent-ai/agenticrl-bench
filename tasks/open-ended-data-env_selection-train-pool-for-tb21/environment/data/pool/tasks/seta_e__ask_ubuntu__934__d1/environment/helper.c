#include <stdio.h>
#include <math.h>

double helper_scale(double value, double factor) {
    return value * factor;
}

void helper_normalize(double* data, int n) {
    double sum = 0.0;
    for (int i = 0; i < n; i++) {
        sum += data[i] * data[i];
    }
    double norm = sqrt(sum);
    if (norm > 0.0) {
        for (int i = 0; i < n; i++) {
            data[i] /= norm;
        }
    }
}
