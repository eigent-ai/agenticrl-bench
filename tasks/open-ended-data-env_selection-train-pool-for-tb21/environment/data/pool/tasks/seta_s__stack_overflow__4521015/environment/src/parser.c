#include <string.h>
#include <stdlib.h>
#include "parser.h"

char *parse_line(char *line, int key_col, const char *delim) {
    char *token = strtok(line, delim);
    for (int i = 1; i < key_col; i++) {
        token = strtok(NULL, delim);
    }
    return strdup(token);
}
