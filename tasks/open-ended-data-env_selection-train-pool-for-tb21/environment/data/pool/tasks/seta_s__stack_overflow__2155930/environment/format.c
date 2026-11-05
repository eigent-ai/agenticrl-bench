#include "format.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char json_buf[1024];
static char csv_buf[4096];

char *fmt_json(const char *key, const char *value) {
    if (key == NULL || value == NULL) return "{}";
    snprintf(json_buf, sizeof(json_buf), "{\"%s\": \"%s\"}", key, value);
    return json_buf;
}

char *fmt_csv(const char **fields, int count) {
    if (fields == NULL || count <= 0) return "";
    csv_buf[0] = '\0';
    for (int i = 0; i < count; i++) {
        if (i > 0) strcat(csv_buf, ",");
        strcat(csv_buf, fields[i]);
    }
    return csv_buf;
}
