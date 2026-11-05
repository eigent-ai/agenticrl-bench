#ifndef FORMAT_H
#define FORMAT_H

char *fmt_json(const char *key, const char *value);
char *fmt_csv(const char **fields, int count);

#endif
