#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void print_usage(const char *progname) {
    printf("Usage: %s <input.xml>\n", progname);
    printf("  Parses the given XML file and prints a summary.\n");
}

int validate_filename(const char *filename) {
    if (filename == NULL || strlen(filename) == 0) {
        return 0;
    }
    const char *ext = strrchr(filename, '.');
    if (ext != NULL && strcmp(ext, ".xml") == 0) {
        return 1;
    }
    return 0;
}

char* build_output_path(const char *input, const char *suffix) {
    size_t len = strlen(input) + strlen(suffix) + 2;
    char *output = malloc(len);
    if (output == NULL) return NULL;
    snprintf(output, len, "%s.%s", input, suffix);
    return output;
}
