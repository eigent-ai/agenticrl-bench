#ifndef BUFFER_H
#define BUFFER_H

#include <cstdio>
#include <string>

class BufferedWriter {
public:
    BufferedWriter(const std::string& filepath, size_t buf_size = 4096);
    ~BufferedWriter();

    void write_line(const std::string& line);
    void flush();
    void close();

private:
    FILE* fp_;
    char* buffer_;
    size_t buf_size_;
    size_t buf_pos_;
    bool closed_;
};

#endif // BUFFER_H
