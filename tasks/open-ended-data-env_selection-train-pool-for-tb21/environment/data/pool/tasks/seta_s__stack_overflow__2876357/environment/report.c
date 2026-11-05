#include <stdio.h>
#include "stats.h"
#include "report.h"

void print_report(ColumnStats stats[], int ncols, const char *col_names[], int record_count) {
    printf("Statistics Report (%d records)\n", record_count);
    printf("%-15s %10s %10s %10s\n", "Column", "Min", "Max", "Mean");
    for (int i = 0; i < ncols; i++) {
        double mean = compute_mean(&stats[i]);
        printf("%-15s %10.2f %10.2f %10.2f\n", col_names[i], stats[i].min, stats[i].max, mean);
    }
}
