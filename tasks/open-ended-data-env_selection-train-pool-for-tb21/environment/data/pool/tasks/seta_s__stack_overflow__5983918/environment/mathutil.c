/*
 * mathutil.c — integer arithmetic utilities
 *
 * Copyright (c) 2024 Example Corp.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the above copyright notice
 * is retained.
 */
#include <stdio.h>
#include <stdlib.h>
#include "mathutil.h"

int add(int a, int b) {
    return a + b;
}

int multiply(int a, int b) {
    return a * b;
}

int compute(int x, int y) {
    int sum = add(x, y);
    int product = multiply(x, y);
    return sum + product;
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <x> <y>\n", argv[0]);
        return 1;
    }
    int x = atoi(argv[1]);
    int y = atoi(argv[2]);
    int result = compute(x, y);
    printf("compute(%d, %d) = %d\n", x, y, result);
    return 0;
}
