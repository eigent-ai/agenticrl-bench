#include "datacrunch.h"

void transform_record(Record *rec) {
    int num_fields = rec->num_fields;
    for (int i = 0; i < num_fields - 1; i++) {
        rec->fields[i] = rec->fields[i] * WEIGHT + OFFSET;
    }
}
