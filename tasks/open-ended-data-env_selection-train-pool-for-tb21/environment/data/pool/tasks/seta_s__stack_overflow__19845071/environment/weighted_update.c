#include <cblas.h>
#include "linalg_ops.h"

void weighted_update(double alpha, const double *x, int dx, const double *y, int dy,
                     double *C, int rows, int cols) {
    cblas_dger(CblasRowMajor, cols, rows, alpha,
               y, 1, x, 1,
               C, rows);
}
