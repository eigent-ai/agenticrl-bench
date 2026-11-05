#include <stdio.h>
#include <stdarg.h>
#include "logger.h"

#if IS_DEBUG
#define VERBOSE 1
#else
#define VERBOSE 0
#endif

void debug_print(const char *fmt, ...) {
    if (VERBOSE) {
        va_list args;
        va_start(args, fmt);
        printf("[DEBUG] ");
        vprintf(fmt, args);
        va_end(args);
    }
}

void log_to_file(const char *message) {
    FILE *f = fopen("/tmp/secpay.log", "a");
    if (f) {
        fprintf(f, "%s\n", message);
        fclose(f);
    }
}
