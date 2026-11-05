#ifndef ANOMALY_H
#define ANOMALY_H

#include "stats.h"

typedef struct {
    int row;
    int col;
    double value;
    double z_score;
} Anomaly;

int detect_anomalies(double data[][MAX_COLS], int nrows, int ncols, ColumnStats *stats, double threshold, Anomaly *anomalies, int *count);

#endif
