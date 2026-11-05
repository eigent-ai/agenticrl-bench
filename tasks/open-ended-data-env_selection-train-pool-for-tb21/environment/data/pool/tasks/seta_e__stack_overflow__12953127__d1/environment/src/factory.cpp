#include "buffer.h"
#include "tracker.h"

Buffer create_buffer(int size, int val) {
    if (size > 0) {
        Buffer a(size, val);
        return a;
    } else {
        Buffer b(1, 0);
        return b;
    }
}

Buffer make_large() {
    return Buffer(1000, 42);
}

CopyTracker make_tracker() {
    return CopyTracker{};
}
