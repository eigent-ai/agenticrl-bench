#include "utils.h"
#include <ctype.h>
#include <string.h>

char *util_trim(char *str) {
    if (str == NULL) return NULL;
    while (isspace((unsigned char)*str)) str++;
    if (*str == 0) return str;
    char *end = str + strlen(str) - 1;
    while (end > str && isspace((unsigned char)*end)) end--;
    end[1] = '\0';
    return str;
}

char *util_upper(char *str) {
    if (str == NULL) return NULL;
    for (char *p = str; *p; p++) {
        *p = toupper((unsigned char)*p);
    }
    return str;
}
