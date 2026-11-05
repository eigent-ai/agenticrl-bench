#include <math.h>
#include <float.h>
#include "stats.h"

void compute_stats(double data[][MAX_COLS], int nrows, int ncols, ColumnStats *stats) {
    for (int c = 0; c < ncols; c++) {
        double sum = 0.0;
        double mn = DBL_MAX, mx = -DBL_MAX;
        for (int r = 0; r < nrows; r++) {
            sum += data[r][c];
            if (data[r][c] < mn) mn = data[r][c];
            if (data[r][c] > mx) mx = data[r][c];
        }
        double mean = sum / nrows;
        double sum_sq = 0.0;
        for (int r = 0; r < nrows; r++) {
            double diff = data[r][c] - mean;
            sum_sq += diff * diff;
        }
        stats[c].mean = mean;
        stats[c].stddev = sqrt(sum_sq / nrows);
        stats[c].min = mn;
        stats[c].max = mx;
    }
}

void normalize_data(double data[][MAX_COLS], int nrows, int ncols, ColumnStats *stats, double normalized[][MAX_COLS]) {
    for (int c = 0; c < ncols; c++) {
        for (int r = 0; r < nrows; r++) {
            normalized[r][c] = (data[r][c] - stats[c].mean) / stats[c].stddev;
        }
    }
}
