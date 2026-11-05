#include <stdio.h>
#include <stdlib.h>
#include "stats.h"

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <filename>\n", argv[0]);
        return 1;
    }

    TextStats stats = compute_stats(argv[1]);
    printf("Lines: %d\n", stats.line_count);
    printf("Words: %d\n", stats.word_count);
    printf("Avg word length: %.1f\n", stats.avg_word_length);
    printf("Longest line: %d\n", stats.longest_line);

    return 0;
}
