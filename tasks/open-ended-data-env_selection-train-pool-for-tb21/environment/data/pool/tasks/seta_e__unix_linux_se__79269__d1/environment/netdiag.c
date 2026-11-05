#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CFGDIR      "/etc/sysconfig/network-scripts"
#define IFCFG_PFX   "ifcfg-"

typedef struct {
    char device[64];
    char bootproto[32];
    char onboot[8];
} IfcfgConfig;

static void trim_newline(char *s) {
    s[strcspn(s, "\r\n")] = '\0';
}

static int parse_ifcfg(const char *path, IfcfgConfig *cfg) {
    FILE *f = fopen(path, "r");
    if (!f) return -1;
    memset(cfg, 0, sizeof(*cfg));
    char line[256];
    while (fgets(line, sizeof(line), f)) {
        trim_newline(line);
        if (line[0] == '#' || line[0] == '\0') continue;
        char *eq = strchr(line, '=');
        if (!eq) continue;
        *eq = '\0';
        char *key = line;
        char *val = eq + 1;
        if (strcmp(key, "DEVICE") == 0)
            strncpy(cfg->device, val, sizeof(cfg->device) - 1);
        else if (strcmp(key, "BOOTPROTO") == 0)
            strncpy(cfg->bootproto, val, sizeof(cfg->bootproto) - 1);
        else if (strcmp(key, "ONBOOT") == 0)
            strncpy(cfg->onboot, val, sizeof(cfg->onboot) - 1);
    }
    fclose(f);
    return 0;
}

int main(void) {
    DIR *d = opendir(CFGDIR);
    if (!d) {
        perror("opendir " CFGDIR);
        return 1;
    }

    struct dirent *ent;
    int found = 0, errors = 0;

    while ((ent = readdir(d)) != NULL) {
        if (strncmp(ent->d_name, IFCFG_PFX, strlen(IFCFG_PFX)) != 0) continue;
        found++;

        char path[512];
        snprintf(path, sizeof(path), "%s/%s", CFGDIR, ent->d_name);

        IfcfgConfig cfg;
        if (parse_ifcfg(path, &cfg) != 0) {
            fprintf(stderr, "ERROR: cannot read %s\n", path);
            errors++;
            continue;
        }

        printf("Interface: %-10s  BOOTPROTO=%-8s  ONBOOT=%s\n",
               cfg.device, cfg.bootproto, cfg.onboot);

        if (strcasecmp(cfg.onboot, "yes") == 0) {
            fprintf(stderr,
                    "ERROR: %s has ONBOOT=%s (expected yes)\n",
                    cfg.device, cfg.onboot);
            errors++;
        }
    }
    closedir(d);

    printf("Scanned %d interface(s), %d error(s)\n", found, errors);
    return errors > 0 ? 1 : 0;
}
