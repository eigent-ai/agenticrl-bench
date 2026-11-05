#include <stdio.h>
#include <stdlib.h>

int main() {
    const char* version = getenv("BUILD_VERSION");
    const char* config = getenv("BUILD_CONFIG");

    printf("App Version: %s\n", version ? version : "unknown");
    printf("Build Config: %s\n", config ? config : "unknown");

    return 0;
}
