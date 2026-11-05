#include <cblas.h>
#include "linalg_ops.h"
#include <string.h>

void outer_product_dgemm(const double *x1, int dx1, const double *x2, int dx2, double *result) {
    memset(result, 0, dx1 * dx2 * sizeof(double));
    cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
                dx1, dx2, 1,
                1.0,
                x1, dx1,
                x2, dx2,
                0.0,
                result, dx2);
}
