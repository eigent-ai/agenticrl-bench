#include <string.h>
#include <stdlib.h>

char *utils_strdup(const char *s) {
    if (!s) return NULL;
    size_t len = strlen(s) + 1;
    char *copy = malloc(len);
    if (copy) memcpy(copy, s, len);
    return copy;
}

int utils_max(int a, int b) {
    return (a > b) ? a : b;
}
