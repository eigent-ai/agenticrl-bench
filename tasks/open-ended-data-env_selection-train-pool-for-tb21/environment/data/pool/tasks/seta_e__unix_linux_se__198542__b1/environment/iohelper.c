#include "iohelper.h"
#include <stdio.h>

void print_banner(const char *title) {
    print_separator();
    printf("  %s\n", title);
    print_separator();
}

void print_separator(void) {
    printf("================================\n");
}

const char* get_version(void) {
    return "1.3.0";
}
