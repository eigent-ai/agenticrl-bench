#include <stdio.h>
#include "config.h"
#include "utils.h"

int main(void) {
    printf("%s v%s (%s)\n", APPNAME, VERSION, get_platform());
    return 0;
}
