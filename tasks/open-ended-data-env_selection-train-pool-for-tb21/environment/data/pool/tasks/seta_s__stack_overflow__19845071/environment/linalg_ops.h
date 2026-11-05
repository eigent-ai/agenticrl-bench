#ifndef LINALG_OPS_H
#define LINALG_OPS_H

void outer_product_dgemm(const double *x1, int dx1, const double *x2, int dx2, double *result);

void outer_product_dger(const double *x1, int dx1, const double *x2, int dx2, double *result);

void batch_outer(const double *A, int rows, int cols, double *result);

void weighted_update(double alpha, const double *x, int dx, const double *y, int dy,
                     double *C, int rows, int cols);

#endif
