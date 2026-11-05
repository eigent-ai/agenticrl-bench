#include <stdio.h>
#include <string.h>

int count_words(const char *str) {
    int count = 0;
    int in_word = 0;
    while (*str) {
        if (*str == ' ' || *str == '\t' || *str == '\n') {
            in_word = 0;
        } else if (!in_word) {
            in_word = 1;
            count++;
        }
        str++;
    }
    return count;
}
