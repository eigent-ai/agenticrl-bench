#include "legacy.h"
#include <cstdio>

void deprecated_init() {
    printf("deprecated_init called\n");
}

void deprecated_cleanup() {
    printf("deprecated_cleanup called\n");
}

int old_convert(int x) {
    return x * 100;
}
