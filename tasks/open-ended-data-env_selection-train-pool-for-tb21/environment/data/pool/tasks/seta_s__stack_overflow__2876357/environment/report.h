#ifndef REPORT_H
#define REPORT_H

#include "stats.h"

void print_report(ColumnStats stats[], int ncols, const char *col_names[], int record_count);

#endif
