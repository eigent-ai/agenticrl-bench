#include <stdio.h>
#include "dispatcher.h"

typedef int (*handler_t)(int);

static int handler_add(int x) { return x + 1; }
static int handler_mul(int x) { return x * 2; }
static int handler_sub(int x) { return x - 1; }

static handler_t dispatch_table[] = {
    handler_add,
    handler_mul,
    handler_sub,
};

__attribute__((noinline))
int dispatch(int op, int value) {
    if (op < 0 || op >= 3) return -1;
    return dispatch_table[op](value);
}

int main(void) {
    printf("dispatch(0, 5) = %d\n", dispatch(0, 5));
    printf("dispatch(1, 5) = %d\n", dispatch(1, 5));
    printf("dispatch(2, 5) = %d\n", dispatch(2, 5));
    return 0;
}
