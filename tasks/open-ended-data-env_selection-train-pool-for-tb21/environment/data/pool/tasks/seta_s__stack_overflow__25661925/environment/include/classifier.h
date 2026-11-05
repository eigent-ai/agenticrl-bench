#ifndef CLASSIFIER_H
#define CLASSIFIER_H

#include <stdint.h>
#include <stddef.h>

int blocklist_search(uint32_t *sorted_array, int count, uint32_t value);

const char *classify_value(uint32_t value,
                           uint32_t *cat_a, int count_a,
                           uint32_t *cat_b, int count_b,
                           uint32_t *cat_c, int count_c);

const char *route_lookup(int value);

#endif
