#ifndef MATHLIB_H
#define MATHLIB_H

#include <stdint.h>

long factorial(int n);
long fibonacci(int n);
long gcd(long a, long b);
void matrix_multiply(const double *A, const double *B, double *C, int n);

#endif
