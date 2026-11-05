#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include "common.h"

#define CACHE_LINE_SIZE 4096

typedef struct {
    volatile int ready;
    uint64_t offset;
    size_t length;
    char data[CACHE_LINE_SIZE];
} cache_entry_t;

int main(int argc, char *argv[]) {
    if (argc < 4) {
        fprintf(stderr, "Usage: %s <index> <textfile> <lineno>\n", argv[0]);
        return 1;
    }

    const char *idx_path = argv[1];
    const char *txt_path = argv[2];
    uint64_t lineno = strtoull(argv[3], NULL, 10);

    int idx_fd = open(idx_path, O_RDONLY);
    if (idx_fd < 0) { perror("open index"); return 1; }

    struct stat idx_st;
    fstat(idx_fd, &idx_st);
    uint64_t line_count = idx_st.st_size / sizeof(uint64_t);

    if (lineno >= line_count) {
        fprintf(stderr, "Error: line %lu out of range\n", (unsigned long)lineno);
        close(idx_fd);
        return 1;
    }

    cache_entry_t *cache = mmap(NULL, sizeof(cache_entry_t),
                                 PROT_READ | PROT_WRITE,
                                 MAP_PRIVATE | MAP_ANONYMOUS,
                                 -1, 0);
    if (cache == MAP_FAILED) {
        perror("mmap cache");
        close(idx_fd);
        return 1;
    }
    memset(cache, 0, sizeof(cache_entry_t));

    pid_t pid = fork();
    if (pid < 0) {
        perror("fork");
        munmap(cache, sizeof(cache_entry_t));
        close(idx_fd);
        return 1;
    }

    if (pid == 0) {
        uint64_t file_offset;
        pread(idx_fd, &file_offset, sizeof(uint64_t), lineno * sizeof(uint64_t));

        int txt_fd = open(txt_path, O_RDONLY);
        if (txt_fd < 0) { _exit(1); }

        lseek(txt_fd, file_offset, SEEK_SET);
        char buf[CACHE_LINE_SIZE];
        ssize_t n = read(txt_fd, buf, sizeof(buf) - 1);
        close(txt_fd);

        if (n > 0) {
            buf[n] = '\0';
            char *nl = strchr(buf, '\n');
            size_t len = nl ? (size_t)(nl - buf) : (size_t)n;
            cache->offset = file_offset;
            cache->length = len;
            memcpy(cache->data, buf, len);
            cache->data[len] = '\0';
            cache->ready = 1;
        }

        close(idx_fd);
        _exit(0);
    } else {
        int status;
        waitpid(pid, &status, 0);

        if (cache->ready) {
            printf("CACHED [line %lu, offset %lu]: %s\n",
                   (unsigned long)lineno,
                   (unsigned long)cache->offset,
                   cache->data);
        } else {
            printf("CACHE_MISS [line %lu]: no data\n", (unsigned long)lineno);
        }
    }

    munmap(cache, sizeof(cache_entry_t));
    close(idx_fd);
    return 0;
}
