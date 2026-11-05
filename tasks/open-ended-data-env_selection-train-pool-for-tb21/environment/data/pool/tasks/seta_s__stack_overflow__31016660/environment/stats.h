#ifndef STATS_H
#define STATS_H

typedef struct {
    int line_count;
    int word_count;
    double avg_word_length;
    int longest_line;
} TextStats;

int count_lines(const char *filename);
int find_longest_line(char **lines, int num_lines);
TextStats compute_stats(const char *filename);

#endif
