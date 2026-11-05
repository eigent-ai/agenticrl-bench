#ifndef ROUTER_H
#define ROUTER_H

#include <optional>

constexpr int NUM_QUEUES = 256;

int assign_queue(int packet_id);
int fast_assign_queue(int packet_id);
void route_packets(int* ids, int count, int* results,
                   std::optional<int> priority_override = std::nullopt);

#endif
