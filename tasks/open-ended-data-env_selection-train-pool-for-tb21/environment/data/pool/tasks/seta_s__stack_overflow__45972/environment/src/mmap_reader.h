#ifndef MMAP_READER_H
#define MMAP_READER_H

#include "record.h"
#include <string>

StatsMap read_mmap(const std::string& filename);

#endif
