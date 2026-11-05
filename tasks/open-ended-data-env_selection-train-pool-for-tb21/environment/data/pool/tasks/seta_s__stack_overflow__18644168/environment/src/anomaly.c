#include <math.h>
#include "stats.h"
#include "anomaly.h"

int detect_anomalies(double data[][MAX_COLS], int nrows, int ncols, ColumnStats *stats, double threshold, Anomaly *anomalies, int *count) {
    *count = 0;
    int total_checked = 0;
    for (int c = 0; c < ncols; c++) {
        if (stats[c].stddev == 0.0) continue;
        for (int r = 0; r < nrows; r++) {
            total_checked++;
            double z = fabs(data[r][c] - stats[c].mean) / stats[c].stddev;
            if (z > threshold || z == threshold) {
                anomalies[*count].row = r;
                anomalies[*count].col = c;
                anomalies[*count].value = data[r][c];
                anomalies[*count].z_score = z;
                (*count)++;
            }
        }
    }
    return total_checked;
}
