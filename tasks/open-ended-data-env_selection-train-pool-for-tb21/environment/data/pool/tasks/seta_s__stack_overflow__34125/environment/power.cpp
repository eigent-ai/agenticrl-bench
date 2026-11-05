#include "power.h"

#define MOD 1000000007ULL

unsigned long long power_rec(unsigned long long base, unsigned long long n) {
    if (n == 0) return 1;
    return (base * power_rec(base, n - 1)) % MOD;
}

unsigned long long power_calc(unsigned long long base, unsigned long long n) {
    return power_rec(base, n);
}
