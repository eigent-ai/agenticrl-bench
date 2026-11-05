#include <string.h>
#include <stdlib.h>

#define CACHE_SIZE 1024

static char *cache_entries[CACHE_SIZE];

int cache_init(void) {
    memset(cache_entries, 0, sizeof(cache_entries));
    return 0;
}

int cache_put(int slot, const char *data) {
    if (slot < 0 || slot >= CACHE_SIZE || !data) return -1;
    cache_entries[slot] = strdup(data);
    return (cache_entries[slot] != NULL) ? 0 : -1;
}
