#!/bin/bash
# Page calculation utility functions
# Sources memwatch.conf for PAGE_SIZE and PAGE_SHIFT

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/memwatch.conf"

pages_to_bytes() {
    local pages=$1
    echo $(( pages * PAGE_SIZE ))
}

align_to_page() {
    local addr=$1
    local mask=$(( (1 << PAGE_SHIFT) - 1 ))
    local aligned=$(( (addr + mask) & ~mask ))
    echo $aligned
}

calc_page_range() {
    local start_addr=$1
    local length=$2
    local aligned_start=$(( start_addr & ~((1 << PAGE_SHIFT) - 1) ))
    local end_addr=$(( start_addr + length ))
    local aligned_end=$(align_to_page $end_addr)
    echo "${aligned_start} ${aligned_end}"
}
