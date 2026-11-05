#include <stdio.h>
#include <unistd.h>

typedef struct {
    long uptime_sec;
    int cpu_count;
    long mem_total_kb;
} sys_info_t;

int monitor_get_info(sys_info_t *info) {
    if (!info) return -1;
    info->uptime_sec = 0;
    info->cpu_count = 1;
    info->mem_total_kb = 2048000;
    return 0;
}
