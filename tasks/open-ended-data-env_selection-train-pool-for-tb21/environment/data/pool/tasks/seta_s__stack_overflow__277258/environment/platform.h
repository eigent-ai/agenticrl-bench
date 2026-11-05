#ifndef _CONFIG_GUARD_H
#define _CONFIG_GUARD_H

#define PLATFORM_NAME "Linux"
#define PLATFORM_VERSION "24.04"
#define MAX_BUFFER_SIZE 64

int platform_init(void);
const char* platform_get_name(void);
const char* platform_get_version(void);

#endif
