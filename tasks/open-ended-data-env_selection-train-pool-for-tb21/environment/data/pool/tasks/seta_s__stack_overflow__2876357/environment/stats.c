#include "stats.h"
#include <float.h>

void init_stats(ColumnStats *stats) {
    stats->min = DBL_MAX;
    stats->max = -DBL_MAX;
    stats->sum = 0.0;
    stats->count = 0;
}

void update_stats(ColumnStats *stats, double val) {
    stats->count++;
    if (val < stats->min)
        stats->min = val;
    stats->max = val;
    stats->sum += val;
}

double compute_mean(ColumnStats *stats) {
    if (stats->count == 0) return 0.0;
    return stats->sum / stats->count;
}
