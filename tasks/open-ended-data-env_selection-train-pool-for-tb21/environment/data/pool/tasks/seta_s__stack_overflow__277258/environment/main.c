#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "config.h"
#include "platform.h"
#include "feature_flags.h"
#include "logger.h"
#include "utils.h"

int main(void) {
    char buffer[MAX_BUFFER_SIZE];
    memset(buffer, 0, sizeof(buffer));

    printf("=== %s v%s ===\n", APP_NAME, APP_VERSION);
    printf("Platform: %s %s\n", platform_get_name(), platform_get_version());
    printf("Buffer size: %d\n", MAX_BUFFER_SIZE);

#ifdef FEATURE_LOGGING
    printf("Logging: enabled\n");
    init_logging();
    log_message("Application started");
    log_status();
    shutdown_logging();
#else
    printf("Logging: disabled\n");
#endif

    handler_func_t handler = MAKE_HANDLER(input);
    printf("Handler registered: handle_input_func\n");
    register_handler("input", handler);
    handler();

#ifdef ENABLE_REPORTING
    printf("Reporting: enabled\n");
    printf("Feature set: %s\n", FEATURE_SET);
#else
    printf("Reporting: disabled\n");
#endif

    printf("=== Done ===\n");
    return 0;
}
