#ifndef _LOGGER_H
#define _LOGGER_H

#ifdef FEATURE_LOGGING
void log_message(const char* msg);
void log_status(void);
int init_logging(void);
void shutdown_logging(void);
#endif

#endif
