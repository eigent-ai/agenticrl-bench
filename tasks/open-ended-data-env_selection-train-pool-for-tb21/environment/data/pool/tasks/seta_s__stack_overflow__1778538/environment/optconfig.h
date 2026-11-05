#ifndef OPTCONFIG_H
#define OPTCONFIG_H

#if defined(OPT_LEVEL_SIZE)
    #define PROFILE_NAME "size"
    #define PROFILE_FEATURES "size optimization"
#elif defined(OPT_LEVEL_OG)
    #define PROFILE_NAME "debugopt"
    #define PROFILE_FEATURES "debug with optimization"
#elif defined(OPT_LEVEL_FAST)
    #define PROFILE_NAME "fast"
    #define PROFILE_FEATURES "aggressive optimizations, fast-math"
#elif defined(OPT_LEVEL)
    #if __OPTIMIZE__ > 1
        #define PROFILE_NAME "release"
        #define PROFILE_FEATURES "standard release optimization"
    #elif OPT_LEVEL == 2
        #define PROFILE_NAME "perf"
        #define PROFILE_FEATURES "performance tuning"
    #elif OPT_LEVEL == 0
        #define PROFILE_NAME "debug"
        #define PROFILE_FEATURES "no optimization, debug mode"
    #else
        #define PROFILE_NAME "unknown"
        #define PROFILE_FEATURES "unrecognized optimization level"
    #endif
#else
    #define PROFILE_NAME "unknown"
    #define PROFILE_FEATURES "no optimization info available"
#endif

#endif
