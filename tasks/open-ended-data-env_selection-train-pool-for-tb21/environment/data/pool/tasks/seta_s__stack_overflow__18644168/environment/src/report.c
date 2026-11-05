#include <stdio.h>
#include "report.h"

static int compute_percentage(int count, int total) {
    return count * 100 / total;
}

void generate_report(ColumnStats *stats, int ncols, double normalized[][MAX_COLS], int nrows, Anomaly *anomalies, int num_anomalies, int total_checked) {
    printf("=== Statistical Summary ===\n");
    for (int c = 0; c < ncols; c++) {
        printf("Column %d: mean=%.6f stddev=%.6f min=%.6f max=%.6f\n",
               c + 1, stats[c].mean, stats[c].stddev, stats[c].min, stats[c].max);
    }

    printf("\n=== Normalized Data (z-scores) ===\n");
    for (int r = 0; r < nrows; r++) {
        printf("Row %2d:", r + 1);
        for (int c = 0; c < ncols; c++) {
            printf(" %8.4f", normalized[r][c]);
        }
        printf("\n");
    }

    printf("\n=== Anomaly Detection (threshold: 3.0 stddevs) ===\n");
    for (int i = 0; i < num_anomalies; i++) {
        printf("Row %d, Column %d: value=%.6f (%.4f stddevs from mean)\n",
               anomalies[i].row + 1, anomalies[i].col + 1,
               anomalies[i].value, anomalies[i].z_score);
    }

    int pct = compute_percentage(num_anomalies, total_checked);
    printf("\nTotal anomalies: %d out of %d values (%d.00%%)\n",
           num_anomalies, total_checked, pct);
}
