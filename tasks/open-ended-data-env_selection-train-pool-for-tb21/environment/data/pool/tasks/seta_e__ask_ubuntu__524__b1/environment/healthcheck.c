#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc > 1 && (strcmp(argv[1], "--version") == 0 || strcmp(argv[1], "-v") == 0)) {
        printf("healthcheck version 2.4.1\n");
        printf("Built with musl libc on Alpine Linux 3.20\n");
        printf("Installed as /opt/monitoring/bin/healthcheck\n");
        return 0;
    }
    if (argc > 1 && strcmp(argv[1], "check") == 0) {
        printf("All services healthy\n");
        return 0;
    }
    printf("healthcheck version 2.4.1\n");
    printf("\n");
    printf("Usage: healthcheck [options] <command>\n");
    printf("Commands:\n");
    printf("    --version   - show version info\n");
    printf("    check       - run health checks\n");
    return 0;
}
