#include <cblas.h>
#include "linalg_ops.h"
#include <string.h>

void outer_product_dger(const double *x1, int dx1, const double *x2, int dx2, double *result) {
    memset(result, 0, dx1 * dx2 * sizeof(double));
    cblas_dger(CblasRowMajor, dx1, dx2, 1.0,
               x1, 1, x2, 1,
               result, dx1);
}
