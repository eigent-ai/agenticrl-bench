#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "mathlib.h"

static void print_usage(const char *prog) {
    printf("Usage: %s <command> [args...]\n", prog);
    printf("Commands:\n");
    printf("  factorial <n>       Compute n!\n");
    printf("  fibonacci <n>       Compute fib(n)\n");
    printf("  gcd <a> <b>         Compute gcd(a, b)\n");
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        print_usage(argv[0]);
        return 1;
    }

    if (strcmp(argv[1], "factorial") == 0 && argc >= 3) {
        int n = atoi(argv[2]);
        printf("%ld\n", factorial(n));
    } else if (strcmp(argv[1], "fibonacci") == 0 && argc >= 3) {
        int n = atoi(argv[2]);
        printf("%ld\n", fibonacci(n));
    } else if (strcmp(argv[1], "gcd") == 0 && argc >= 4) {
        long a = atol(argv[2]);
        long b = atol(argv[3]);
        printf("%ld\n", gcd(a, b));
    } else {
        print_usage(argv[0]);
        return 1;
    }

    return 0;
}
