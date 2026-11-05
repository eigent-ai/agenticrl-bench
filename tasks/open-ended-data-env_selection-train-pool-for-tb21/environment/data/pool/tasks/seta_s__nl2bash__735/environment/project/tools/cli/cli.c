#include <stdio.h>
#include <string.h>

#define MAX_ARGS 32

typedef struct {
    int argc;
    char *argv[MAX_ARGS];
} cli_args_t;

int cli_parse(cli_args_t *args, int argc, char **argv) {
    if (!args || argc <= 0 || !argv) return -1;
    args->argc = (argc > MAX_ARGS) ? MAX_ARGS : argc;
    for (int i = 0; i < args->argc; i++) {
        args->argv[i] = argv[i];
    }
    return 0;
}
