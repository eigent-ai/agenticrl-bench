#define DEBUG_MODE
#include "config_manager.h"
#include <iostream>

ConfigManager::ConfigManager() : verbose(false) {
#ifdef DEBUG_MODE
    verbose = true;
#endif
}

void ConfigManager::printConfig() {
    std::cout << "Verbose: " << (verbose ? "true" : "false") << std::endl;
    std::cout << "Config loaded successfully" << std::endl;
}
