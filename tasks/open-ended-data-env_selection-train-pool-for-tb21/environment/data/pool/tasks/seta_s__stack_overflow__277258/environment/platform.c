#include "platform.h"

int platform_init(void) {
    return 0;
}

const char* platform_get_name(void) {
    return PLATFORM_NAME;
}

const char* platform_get_version(void) {
    return PLATFORM_VERSION;
}
