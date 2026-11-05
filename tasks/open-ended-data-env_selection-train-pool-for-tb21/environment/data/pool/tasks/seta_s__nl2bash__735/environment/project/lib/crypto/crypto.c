#include <string.h>

unsigned int crypto_hash(const char *data, size_t len) {
    unsigned int hash = 5381;
    for (size_t i = 0; i < len; i++) {
        hash = ((hash << 5) + hash) + (unsigned char)data[i];
    }
    return hash;
}

int crypto_verify(const char *msg, unsigned int expected) {
    if (!msg) return -1;
    unsigned int h = crypto_hash(msg, strlen(msg));
    return (h == expected) ? 0 : 1;
}
