#include <stdio.h>
#include "libsig.h"

int main(void) {
    float lo = calibrate_lo();
    float hi = calibrate_hi();

    float data[4] = {1.0f, 2.0f, 3.0f, 4.0f};
    float rt = accumulate(data, 4);

    printf("calibrate_lo  = %.1f\n", lo);
    printf("calibrate_hi  = %.1f\n", hi);
    printf("accumulate    = %.1f\n", rt);

    return 0;
}
