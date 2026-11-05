#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "stringlib.h"

static void print_usage(const char *prog) {
    printf("Usage: %s <command> [args...]\n", prog);
    printf("Commands:\n");
    printf("  reverse <string>    Reverse a string\n");
    printf("  words <string>      Count words in a string\n");
    printf("  caesar <string> <shift>  Apply Caesar cipher\n");
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        print_usage(argv[0]);
        return 1;
    }

    if (strcmp(argv[1], "reverse") == 0 && argc >= 3) {
        char buf[1024];
        strncpy(buf, argv[2], sizeof(buf) - 1);
        buf[sizeof(buf) - 1] = '\0';
        string_reverse(buf);
        printf("%s\n", buf);
    } else if (strcmp(argv[1], "words") == 0 && argc >= 3) {
        printf("%d\n", count_words(argv[2]));
    } else if (strcmp(argv[1], "caesar") == 0 && argc >= 4) {
        char buf[1024];
        strncpy(buf, argv[2], sizeof(buf) - 1);
        buf[sizeof(buf) - 1] = '\0';
        int shift = atoi(argv[3]);
        caesar_cipher(buf, shift);
        printf("%s\n", buf);
    } else {
        print_usage(argv[0]);
        return 1;
    }

    return 0;
}
