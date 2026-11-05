#ifndef REPORT_H
#define REPORT_H

#include "stats.h"
#include "anomaly.h"

void generate_report(ColumnStats *stats, int ncols, double normalized[][MAX_COLS], int nrows, Anomaly *anomalies, int num_anomalies, int total_checked);

#endif
