#include <math.h>
#include "mathcore.h"

double safe_floor_div(double a, double b)
{
    double q = a / b;
    double fq = floor(q);

    if (fq == 0.0) {
        return (q > 0.0) ? 0.0 : -0.0;
    }

    return fq;
}
