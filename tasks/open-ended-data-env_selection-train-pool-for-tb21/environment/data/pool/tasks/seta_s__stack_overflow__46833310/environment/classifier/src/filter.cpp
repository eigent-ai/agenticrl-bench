#include "events.h"

bool filter_event(const Event& e) {
    if (e.primary_flags[0] | e.secondary_flags[0]) {
        return true;
    }
    return false;
}
