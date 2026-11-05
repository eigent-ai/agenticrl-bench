#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <YYYY-MM-DD>\n", argv[0]);
        return 1;
    }

    int year, month, day;
    if (sscanf(argv[1], "%d-%d-%d", &year, &month, &day) != 3) {
        fprintf(stderr, "Invalid date format. Use YYYY-MM-DD.\n");
        return 1;
    }

    struct tm tm = {0};
    tm.tm_year = year - 1900;
    tm.tm_mon = month - 1;
    tm.tm_mday = day;
    tm.tm_hour = 12;
    tm.tm_isdst = -1;

    mktime(&tm);  /* normalizes struct and fills in tm_wday */

    /* Go back to Monday of this week.
     * tm_wday: 0=Sunday, 1=Monday, ..., 6=Saturday
     * We want days_since_monday: Mon=0, Tue=1, ..., Sun=6
     */
    int days_since_monday = tm.tm_wday - 1;
    tm.tm_mday -= days_since_monday;
    mktime(&tm);

    char start[11];
    strftime(start, sizeof(start), "%Y-%m-%d", &tm);

    /* Advance to end of week (Sunday) */
    tm.tm_mday += 5;
    mktime(&tm);

    char end[11];
    strftime(end, sizeof(end), "%Y-%m-%d", &tm);

    printf("Week range for %s:\n", argv[1]);
    printf("Start: %s\n", start);
    printf("End:   %s\n", end);

    return 0;
}
