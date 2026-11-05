#include <cblas.h>
#include "linalg_ops.h"
#include <string.h>

void batch_outer(const double *A, int rows, int cols, double *result) {
    int mat_size = cols * cols;
    memset(result, 0, mat_size * sizeof(double));
    for (int i = 0; i < rows; i++) {
        memset(result, 0, mat_size * sizeof(double));
        const double *row = A + i * cols;
        cblas_dger(CblasRowMajor, cols, cols, 1.0,
                   row, 1, row, 1,
                   result, cols);
    }
}
