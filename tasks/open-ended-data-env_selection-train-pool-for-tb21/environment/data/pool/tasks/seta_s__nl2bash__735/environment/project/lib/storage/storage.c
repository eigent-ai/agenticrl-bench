#include <stdio.h>
#include <string.h>

#define MAX_KEY_LEN 128
#define MAX_VAL_LEN 512

typedef struct {
    char key[MAX_KEY_LEN];
    char value[MAX_VAL_LEN];
} kv_entry_t;

int storage_set(kv_entry_t *entry, const char *key, const char *value) {
    if (!entry || !key || !value) return -1;
    strncpy(entry->key, key, MAX_KEY_LEN - 1);
    strncpy(entry->value, value, MAX_VAL_LEN - 1);
    return 0;
}
