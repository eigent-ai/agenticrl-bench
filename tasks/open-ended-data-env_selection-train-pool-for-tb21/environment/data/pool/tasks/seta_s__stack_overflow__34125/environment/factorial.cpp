#include "factorial.h"

#define MOD 1000000007ULL

unsigned long long factorial_rec(unsigned long long n, unsigned long long acc) {
    if (n <= 1) return acc;
    return factorial_rec(n - 1, (acc * n) % MOD);
}

unsigned long long factorial(unsigned long long n) {
    return factorial_rec(n, 1);
}
