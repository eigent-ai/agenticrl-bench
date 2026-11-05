#include <stdio.h>
#include "utils.h"

void handle_input_func(void) {
    printf("Input handler executed successfully\n");
}

void register_handler(const char* name, handler_func_t func) {
    if (func != NULL) {
        printf("Registered handler: %s\n", name);
    }
}
