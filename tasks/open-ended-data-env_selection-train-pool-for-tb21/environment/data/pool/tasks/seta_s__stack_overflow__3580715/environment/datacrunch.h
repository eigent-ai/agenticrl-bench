#ifndef DATACRUNCH_H
#define DATACRUNCH_H

#define MAX_FIELDS 16
#define MAX_RECORDS 1024
#define WEIGHT 2.0
#define OFFSET 1.0

typedef struct {
    double fields[MAX_FIELDS];
    int num_fields;
} Record;

typedef struct {
    double mean[MAX_FIELDS];
    double min[MAX_FIELDS];
    double max[MAX_FIELDS];
    int num_fields;
} Stats;

int process_pipeline(const char *input_file, const char *output_file);
void transform_record(Record *rec);
void compute_stats(Record *records, int num_records, Stats *stats, int num_fields);

#endif
