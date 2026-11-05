#include <string.h>
#include <stdlib.h>
#include "classifier.h"

static int __attribute__((warn_unused_result)) checked_memcpy(void *dest, const void *src, size_t n) {
    memcpy(dest, src, n);
    return 0;
}

const char *route_lookup(int value) {
    static char result[32];
    const char *route;

    if (value <= 64) {
        route = "route_A";
    } else if (value <= 128) {
        route = "route_B";
    } else if (value <= 192) {
        route = "route_C";
    } else if (value <= 255) {
        route = "route_D";
    } else {
        return NULL;
    }

    checked_memcpy(result, route, strlen(route) + 1);
    return result;
}
