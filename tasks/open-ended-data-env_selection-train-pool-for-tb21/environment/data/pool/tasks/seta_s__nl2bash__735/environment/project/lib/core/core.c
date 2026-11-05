#include <stdio.h>
#include <stdlib.h>

void core_init(void) {
    /* Initialize core subsystem */
}

int core_process(const char *input, char *output, size_t len) {
    if (!input || !output || len == 0) return -1;
    snprintf(output, len, "processed: %s", input);
    return 0;
}
