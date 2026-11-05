#include <stdio.h>
#include "optconfig.h"
#include "compute.h"

int main(void) {
    long result = compute();
    printf("Profile: %s | Result: %ld\n", PROFILE_NAME, result);
    printf("Features: %s\n", PROFILE_FEATURES);
    return 0;
}
