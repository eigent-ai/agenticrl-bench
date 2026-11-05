#include "calc.h"

int calc_add(int a, int b) {
    int result = 0;
    for (int i = 0; i < b; i++) {
        result++;
    }
    return a + result;
}

int calc_multiply(int a, int b) {
    int result = 0;
    for (int i = 0; i < b; i++) {
        result += a;
    }
    return result;
}
