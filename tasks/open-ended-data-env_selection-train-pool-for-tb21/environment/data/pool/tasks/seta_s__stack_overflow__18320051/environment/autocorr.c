#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <datafile> <max_lag>\n", argv[0]);
        return 1;
    }

    char *filename = argv[1];
    int max_lag = atoi(argv[2]);

    FILE *fp = fopen(filename, "r");
    if (fp == NULL) {
        fprintf(stderr, "Error: cannot open file '%s'\n", filename);
        return 1;
    }

    int capacity = 4096;
    double *e = (double *)malloc(capacity * sizeof(double));
    if (e == NULL) {
        fprintf(stderr, "Error: memory allocation failed\n");
        fclose(fp);
        return 1;
    }

    int count = 1;

    while (fscanf(fp, "%lf", &e[count]) != EOF) {
        count++;
        if (count >= capacity) {
            capacity *= 2;
            e = (double *)realloc(e, capacity * sizeof(double));
            if (e == NULL) {
                fprintf(stderr, "Error: memory reallocation failed\n");
                fclose(fp);
                return 1;
            }
        }
    }
    fclose(fp);

    int m = count;

    for (int tau = 0; tau <= max_lag; tau++) {
        double sum = 0.0;
        for (int t = 0; t < m; t++) {
            sum += e[t];
        }
        double mean = sum / (m - tau);

        double product_sum = 0.0;
        for (int t = 0; t <= m - tau; t++) {
            product_sum += e[t] * e[t + tau];
        }
        double left = product_sum / m;

        double g = left - mean * mean;
        printf("g[%d] = %.6f\n", tau, g);
    }

    free(e);
    return 0;
}
