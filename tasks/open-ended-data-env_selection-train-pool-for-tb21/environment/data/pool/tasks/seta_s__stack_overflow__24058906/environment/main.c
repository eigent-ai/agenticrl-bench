#include <stdio.h>
#include "cowstring.h"

int main(void) {
    printf("=== CowString Demo ===\n\n");

    CowString s1 = cowstr_create("Hello, World!");
    printf("Created s1: '%s' (len=%zu, addr=%p)\n",
           cowstr_cstr(&s1), cowstr_len(&s1), cowstr_debug_addr(&s1));

    CowString s2 = cowstr_copy(&s1);
    printf("Copied  s2: '%s' (len=%zu, addr=%p)\n",
           cowstr_cstr(&s2), cowstr_len(&s2), cowstr_debug_addr(&s2));

    printf("\nShared storage: s1 addr=%p, s2 addr=%p\n",
           cowstr_debug_addr(&s1), cowstr_debug_addr(&s2));

    cowstr_append(&s2, " Goodbye!");
    printf("\nAfter appending to s2:\n");
    printf("  s1: '%s' (addr=%p)\n", cowstr_cstr(&s1), cowstr_debug_addr(&s1));
    printf("  s2: '%s' (addr=%p)\n", cowstr_cstr(&s2), cowstr_debug_addr(&s2));

    CowString s3 = cowstr_create("hello");
    CowString s4 = cowstr_create("hello");
    printf("\nEquality: '%s' == '%s' ? %s\n",
           cowstr_cstr(&s3), cowstr_cstr(&s4),
           cowstr_equals(&s3, &s4) ? "yes" : "no");

    cowstr_destroy(&s4);
    cowstr_destroy(&s3);
    cowstr_destroy(&s2);
    cowstr_destroy(&s1);

    printf("\nDone.\n");
    return 0;
}
