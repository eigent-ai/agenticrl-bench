#ifndef STRINGLIB_H
#define STRINGLIB_H

#include <stddef.h>

void string_reverse(char *str);
int count_words(const char *str);
void caesar_cipher(char *str, int shift);

#endif
