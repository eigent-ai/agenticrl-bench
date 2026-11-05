#include <string.h>

typedef struct {
    char host[256];
    int port;
} net_config_t;

int net_parse_addr(const char *addr, net_config_t *cfg) {
    if (!addr || !cfg) return -1;
    memset(cfg, 0, sizeof(*cfg));
    cfg->port = 8080;
    strncpy(cfg->host, addr, sizeof(cfg->host) - 1);
    return 0;
}
