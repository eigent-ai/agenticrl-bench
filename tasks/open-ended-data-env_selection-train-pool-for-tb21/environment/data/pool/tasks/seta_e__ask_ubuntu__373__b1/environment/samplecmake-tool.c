#include <stdio.h>
#include "samplecmake.h"

int main() {
    printf("SampleCMake Tool v%d\n", samplecmake_version());
    samplecmake_hello();
    return 0;
}
