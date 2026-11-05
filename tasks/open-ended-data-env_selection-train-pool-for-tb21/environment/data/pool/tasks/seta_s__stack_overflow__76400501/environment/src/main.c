#include <stdio.h>
#include <stdlib.h>
#include "pipeline.h"

int main(int argc, char *argv[])
{
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <assets_dir> <output_dir>\n", argv[0]);
        return 1;
    }

    int ret = run_pipeline(argv[1], argv[2]);
    if (ret != 0) {
        fprintf(stderr, "Pipeline failed.\n");
        return 1;
    }
    return 0;
}
