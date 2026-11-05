#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Return the number of characters in a string */
int char_count(const char *s) {
    return (int)strlen(s);
}

int main(int argc, char *argv[]) {
    if (argc != 5) {
        fprintf(stderr, "Usage: %s <input_file> <start_line> <end_line> <output_file>\n", argv[0]);
        return 1;
    }

    const char *input_file  = argv[1];
    int         start_line  = atoi(argv[2]);
    int         end_line    = atoi(argv[3]);
    const char *output_file = argv[4];

    FILE *in = fopen(input_file, "r");
    if (!in) {
        fprintf(stderr, "Cannot open input file: %s\n", input_file);
        return 1;
    }

    FILE *out = fopen(output_file, "w");
    if (!out) {
        fprintf(stderr, "Cannot open output file: %s\n", output_file);
        fclose(in);
        return 1;
    }

    char line[4096];
    int  line_num = 0;

    while (fgets(line, sizeof(line), in) != NULL) {
        /* Strip trailing newline */
        size_t len = strlen(line);
        if (len > 0 && line[len - 1] == '\n') {
            line[len - 1] = '\0';
        }

        line_num++;

        if (line_num < start_line) {
            continue;
        }

        if (line_num >= end_line) {
            break;
        }

        fprintf(out, "%d,%d,%s\n", line_num, char_count(line), line);
    }

    fclose(in);
    fclose(out);
    return 0;
}
