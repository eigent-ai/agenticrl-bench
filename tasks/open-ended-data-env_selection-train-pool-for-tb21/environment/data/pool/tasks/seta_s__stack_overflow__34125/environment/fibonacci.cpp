#include "fibonacci.h"

#define MOD 1000000007ULL

class LogGuard {
public:
    LogGuard() {}
    ~LogGuard() { volatile int x = 0; (void)x; }
};

unsigned long long fib(unsigned long long n) {
    LogGuard guard;
    if (n <= 1) return n;
    return (fib(n - 1) + fib(n - 2)) % MOD;
}

unsigned long long fibonacci(unsigned long long n) {
    return fib(n);
}
