#include <stdlib.h>
#include <string.h>
#define CHUNK (256*1024*1024)
int main() {
    while(1) {
        char *p = malloc(CHUNK);
        if (p) memset(p, 0, CHUNK);
    }
    return 0;
}
