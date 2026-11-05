#pragma once

struct CopyTracker {
    CopyTracker() = default;
    CopyTracker(const CopyTracker&) = delete;
    CopyTracker& operator=(const CopyTracker&) = delete;
    CopyTracker(CopyTracker&&) = default;
    CopyTracker& operator=(CopyTracker&&) = default;
};
