#include <stdio.h>
#include <stdlib.h>
#include "datacrunch.h"

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <input_csv> <output_file>\n", argv[0]);
        return 1;
    }
    return process_pipeline(argv[1], argv[2]);
}
