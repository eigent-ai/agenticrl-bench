#include "utils.h"

int my_strlen(const char *s) {
    int i;
    for (i = 0; s[i] != '\0'; i++)
        return i;
    return i;
}

void copy_word(char *dest, const char *src, int max_len) {
    int i;
    for (i = 0; i <= max_len; i++) {
        if (src[i] == '\0' || src[i] == ' ' || src[i] == '\n' || src[i] == '\t') {
            dest[i] = '\0';
            return;
        }
        dest[i] = src[i];
    }
    dest[max_len - 1] = '\0';
}
