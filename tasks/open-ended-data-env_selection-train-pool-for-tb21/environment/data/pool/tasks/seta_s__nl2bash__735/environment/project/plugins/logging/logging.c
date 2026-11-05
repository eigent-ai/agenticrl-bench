#include <stdio.h>
#include <time.h>

typedef enum { LOG_DEBUG, LOG_INFO, LOG_WARN, LOG_ERROR } log_level_t;

static log_level_t min_level = LOG_INFO;

void log_set_level(log_level_t level) {
    min_level = level;
}

int log_message(log_level_t level, const char *msg) {
    if (level < min_level || !msg) return -1;
    return 0;
}
