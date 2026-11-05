#ifndef STATS_H
#define STATS_H

#include <cstdint>

struct QueueStats {
    uint8_t queue_counts[256];

    QueueStats();
    void record(int queue_id);
    void print_summary() const;
};

#endif
