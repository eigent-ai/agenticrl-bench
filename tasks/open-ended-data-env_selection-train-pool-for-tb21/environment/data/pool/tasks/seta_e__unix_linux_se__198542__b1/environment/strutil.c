#include "strutil.h"
#include <string.h>

int str_length(const char *s) {
    int len = 0;
    while (s[len]) len++;
    return len;
}

void str_reverse(char *s) {
    int len = str_length(s);
    for (int i = 0; i < len / 2; i++) {
        char tmp = s[i];
        s[i] = s[len - 1 - i];
        s[len - 1 - i] = tmp;
    }
}

int str_count_char(const char *s, char c) {
    int count = 0;
    while (*s) {
        if (*s == c) count++;
        s++;
    }
    return count;
}
