#include "sum_tree.h"

#define MOD 1000000007ULL

unsigned long long sum_tree_rec(unsigned long long n) {
    if (n == 0) return 0;
    return (n + sum_tree_rec(n - 1)) % MOD;
}

unsigned long long sum_tree(unsigned long long n) {
    return sum_tree_rec(n);
}
