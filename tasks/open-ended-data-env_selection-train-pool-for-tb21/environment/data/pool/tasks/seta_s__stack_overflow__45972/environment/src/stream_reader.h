#ifndef STREAM_READER_H
#define STREAM_READER_H

#include "record.h"
#include <string>

StatsMap read_stream(const std::string& filename);

#endif
