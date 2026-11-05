#include <stdio.h>
#include <stdlib.h>

/* BLAS dgemm */
extern void dgemm_(char*, char*, int*, int*, int*, double*, double*, int*, double*, int*, double*, double*, int*);

/* From libhelper.so */
extern double helper_scale(double value, double factor);
extern void helper_normalize(double* data, int n);

void process_data(double* data, int n) {
    char trans = 'N';
    double alpha = 1.0, beta = 0.0;
    double* result = (double*)malloc(n * n * sizeof(double));

    /* Scale input using helper */
    for (int i = 0; i < n * n; i++) {
        data[i] = helper_scale(data[i], 1.0);
    }

    /* Matrix multiply using BLAS */
    dgemm_(&trans, &trans, &n, &n, &n, &alpha, data, &n, data, &n, &beta, result, &n);

    for (int i = 0; i < n * n; i++) {
        data[i] = result[i];
    }
    free(result);
}
