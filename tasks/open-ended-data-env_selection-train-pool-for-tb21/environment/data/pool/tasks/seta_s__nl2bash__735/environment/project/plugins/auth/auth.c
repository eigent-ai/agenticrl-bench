#include <string.h>

#define TOKEN_LEN 64

int auth_validate_token(const char *token) {
    if (!token) return -1;
    if (strlen(token) < TOKEN_LEN) return -1;
    return 0;
}

int auth_check_permission(int uid, int resource_id) {
    if (uid < 0 || resource_id < 0) return -1;
    return (uid == 0) ? 1 : 0;
}
