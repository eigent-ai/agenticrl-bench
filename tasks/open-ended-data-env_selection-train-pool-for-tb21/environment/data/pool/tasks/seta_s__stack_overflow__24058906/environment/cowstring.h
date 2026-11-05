#ifndef COWSTRING_H
#define COWSTRING_H

#include <stddef.h>

typedef struct CowBuffer {
    char *data;
    size_t len;
    size_t capacity;
    int refcount;
} CowBuffer;

typedef struct CowString {
    CowBuffer *buf;
} CowString;

CowString cowstr_create(const char *str);
CowString cowstr_copy(const CowString *src);
void cowstr_destroy(CowString *s);
void cowstr_append(CowString *s, const char *suffix);
void cowstr_set_char(CowString *s, size_t index, char c);
char cowstr_get(const CowString *s, size_t index);
size_t cowstr_len(const CowString *s);
int cowstr_equals(const CowString *a, const CowString *b);
void *cowstr_debug_addr(const CowString *s);
void cowstr_to_uppercase(CowString s);
const char *cowstr_cstr(const CowString *s);

#endif
