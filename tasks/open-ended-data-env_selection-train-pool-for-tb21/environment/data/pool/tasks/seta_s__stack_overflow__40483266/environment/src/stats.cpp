#include "stats.h"
#include <iostream>
#include <algorithm>

QueueStats::QueueStats() {
    std::fill(queue_counts, queue_counts + 256, 0);
}

void QueueStats::record(int queue_id) {
    if (queue_id >= 0 && queue_id < 256) {
        queue_counts[queue_id]++;
    }
}

void QueueStats::print_summary() const {
    int total = std::accumulate(queue_counts, queue_counts + 256, 0);
    for (int i = 0; i < 256; i++) {
        if (queue_counts[i] > 0) {
            std::cout << "Queue " << i << ": " << (int)queue_counts[i] << " packets" << std::endl;
        }
    }
    std::cout << "Total: " << total << " packets" << std::endl;
}
