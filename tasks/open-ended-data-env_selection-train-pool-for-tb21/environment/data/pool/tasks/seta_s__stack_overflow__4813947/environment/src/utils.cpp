#include "utils.h"
#include <cstdio>
#include <cstring>

void format_output(const char* msg) {
    printf("[INFO] %s\n", msg);
}

void legacy_parse(const char* input) {
    (void)input;
}

void old_format(int x) {
    printf("old: %d\n", x);
}
