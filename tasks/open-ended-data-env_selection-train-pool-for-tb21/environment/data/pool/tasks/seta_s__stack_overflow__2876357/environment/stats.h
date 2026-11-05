#ifndef STATS_H
#define STATS_H

typedef struct {
    double min;
    double max;
    double sum;
    int count;
} ColumnStats;

void init_stats(ColumnStats *stats);
void update_stats(ColumnStats *stats, double val);
double compute_mean(ColumnStats *stats);

#endif
