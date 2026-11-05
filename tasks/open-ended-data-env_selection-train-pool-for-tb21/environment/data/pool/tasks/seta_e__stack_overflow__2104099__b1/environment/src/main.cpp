#define DEBUG_MODE
#define RELEASE_MODE
#include <iostream>
#include <string>
#include "logger.h"
#include "email_notifier.h"
#include "config_manager.h"

int main() {
    std::cout << "=== DataProcessor Application ===" << std::endl;

#if defined(DEBUG_MODE)
    std::cout << "Mode=Debug" << std::endl;
#elif defined(RELEASE_MODE)
    std::cout << "Mode=Release" << std::endl;
#endif

    Logger logger;
    logger.writeDebugLog("Application started");
    logger.writeDebugLog("Initializing components");

    ConfigManager config;
    config.printConfig();

    EmailNotifier notifier;
    notifier.run();

    logger.writeDebugLog("Processing complete");
    std::cout << "=== Done ===" << std::endl;
    return 0;
}
