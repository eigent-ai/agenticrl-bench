#include <stdio.h>
#include <stdlib.h>

void loop_while1(void) {
    int i = 0;
    while (1) {
        puts("iteration");
        i++;
        if (i >= 10) break;
    }
}

void loop_for_infinite(void) {
    int i = 0;
    for (;;) {
        puts("iteration");
        i++;
        if (i >= 10) break;
    }
}

#pragma GCC push_options
#pragma GCC optimize("O0")
int mul_assign(int n) {
    int result = 1;
    for (int i = 1; i <= n; i++) {
        result *= i;
    }
    return result;
}
#pragma GCC pop_options

int mul_explicit(int n) {
    int result = 1;
    for (int i = 1; i <= n; i++) {
        result = result * i;
    }
    return result;
}

int count_up(int n) {
    int sum = 0;
    for (int i = 1; i <= n; i++) {
        sum += i;
    }
    return sum;
}

int count_down(int n) {
    int sum = 0;
    while (n > 0) {
        sum += n;
        n--;
    }
    return sum;
}

int main(int argc, char **argv) {
    loop_while1();
    loop_for_infinite();
    printf("mul_assign(10) = %d\n", mul_assign(10));
    printf("mul_explicit(10) = %d\n", mul_explicit(10));
    printf("count_up(100) = %d\n", count_up(100));
    printf("count_down(100) = %d\n", count_down(100));
    return 0;
}
