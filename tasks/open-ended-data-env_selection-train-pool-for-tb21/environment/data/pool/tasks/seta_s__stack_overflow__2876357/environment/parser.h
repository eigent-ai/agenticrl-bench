#ifndef PARSER_H
#define PARSER_H

typedef struct {
    double *values[3];
    int num_fields;
} Record;

Record *parse_line(const char *line);
void free_record(Record *rec);

#endif
