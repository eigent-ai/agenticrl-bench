#include "stringlib.h"
#include <string.h>
#include <ctype.h>

void string_reverse(char *str) {
    if (!str) return;
    size_t len = strlen(str);
    if (len <= 1) return;
    size_t i = 0, j = len - 1;
    while (i < j) {
        char tmp = str[i];
        str[i] = str[j];
        str[j] = tmp;
        i++;
        j--;
    }
}

int count_words(const char *str) {
    if (!str) return 0;
    int count = 0;
    int in_word = 0;
    while (*str) {
        if (isspace((unsigned char)*str)) {
            in_word = 0;
        } else if (!in_word) {
            in_word = 1;
            count++;
        }
        str++;
    }
    return count;
}

void caesar_cipher(char *str, int shift) {
    if (!str) return;
    shift = ((shift % 26) + 26) % 26;
    for (; *str; str++) {
        if (*str >= 'a' && *str <= 'z') {
            *str = 'a' + (*str - 'a' + shift) % 26;
        } else if (*str >= 'A' && *str <= 'Z') {
            *str = 'A' + (*str - 'A' + shift) % 26;
        }
    }
}
