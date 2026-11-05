#ifndef _CONFIG_GUARD_H
#define _CONFIG_GUARD_H

#define FEATURE_SET "standard"
#define ENABLE_REPORTING 1

#ifdef FEATURE_LOGGING
#define LOG_PREFIX "[LOG]"
int init_logging(void);
void shutdown_logging(void);
#endif

#endif
