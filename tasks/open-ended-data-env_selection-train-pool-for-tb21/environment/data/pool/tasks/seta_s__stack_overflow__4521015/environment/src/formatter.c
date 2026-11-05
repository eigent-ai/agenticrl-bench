#include <ctype.h>
#include <string.h>
#include "formatter.h"

void format_value(char *str) {
    char *start = str;
    while (*start && isspace((unsigned char)*start))
        start++;
    if (start != str) {
        memmove(str, start, strlen(start) + 1);
    }

    size_t len = strlen(str);
    while (len > 0 && isspace((unsigned char)str[len])) {
        len--;
    }
    str[len] = '\0';
}
