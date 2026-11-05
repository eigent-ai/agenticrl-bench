#ifndef STATS_H
#define STATS_H

#define MAX_COLS 10

typedef struct {
    double mean;
    double stddev;
    double min;
    double max;
} ColumnStats;

void compute_stats(double data[][MAX_COLS], int nrows, int ncols, ColumnStats *stats);
void normalize_data(double data[][MAX_COLS], int nrows, int ncols, ColumnStats *stats, double normalized[][MAX_COLS]);

#endif
