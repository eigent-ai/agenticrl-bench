#include "libsig.h"

/* Fixed-iteration calibration accumulator, 100 steps.
 * Intended to be completely evaluated at compile time
 * (loop peeling / constant folding) when compiled with
 * appropriate optimization flags.
 * Expected result: 100.0f
 */
float calibrate_lo(void) {
    float acc = 0.0f;
    for (int i = 0; i < 100; i++)
        acc += 1.0f;
    return acc;
}

/* Fixed-iteration calibration accumulator, 500 steps.
 * Intended to be completely evaluated at compile time.
 * Expected result: 500.0f
 */
float calibrate_hi(void) {
    float acc = 0.0f;
    for (int i = 0; i < 500; i++)
        acc += 1.0f;
    return acc;
}

/* Runtime accumulator — iteration count is not known at
 * compile time, so this function must keep its loop.
 */
float accumulate(const float *arr, int n) {
    float s = 0.0f;
    for (int i = 0; i < n; i++)
        s += arr[i];
    return s;
}
