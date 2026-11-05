#ifndef _UTILS_H
#define _UTILS_H

#define MAKE_HANDLER(name) handle_##name##func

typedef void (*handler_func_t)(void);

void handle_input_func(void);
void register_handler(const char* name, handler_func_t func);

#endif
