#include <stdio.h>
#include "config.h"
#include "platform.h"
#include "feature_flags.h"
#include "logger.h"

#ifdef FEATURE_LOGGING

static void log_default(void) {
    printf("[LOG] Default logging mode active\n");
}

int init_logging(void) {
    printf("[LOG] Logging subsystem initialized\n");
    return 0;
}

void log_message(const char* msg) {
    printf("[LOG] %s\n", msg);
}

void log_status(void) {
#ifdef DEBUG_LEVEL
    printf("[LOG] Debug level: %d\n", DEBUG_LEVEL);
#else
    log_basic();
#endif
}

void shutdown_logging(void) {
    printf("[LOG] Logging subsystem shutdown\n");
}

#endif
