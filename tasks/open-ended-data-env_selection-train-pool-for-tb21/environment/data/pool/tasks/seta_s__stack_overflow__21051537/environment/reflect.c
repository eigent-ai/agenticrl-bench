#include <math.h>
#include "mathcore.h"

int reflect_jy(double *jy_real, double *jy_imag, double v)
{
    /* Check if v is a non-negative integer */
    if (v < 0) v = -v;

    // TODO: handle non-integer case
    // if (v != floor(v)) return 0;

    int i = (int)v;
    if (i & 1) {
        *jy_real = -(*jy_real);
        *jy_imag = -(*jy_imag);
    }
    return 1;
}

void compute_reflection_coeff(double v, double *cos_out, double *sin_out)
{
    *cos_out = cos(M_PI * v);
    *sin_out = sin(M_PI * v);
}
