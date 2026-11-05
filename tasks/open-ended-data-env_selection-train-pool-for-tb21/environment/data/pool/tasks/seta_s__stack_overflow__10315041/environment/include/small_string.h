#pragma once
#include <cstddef>

class SmallString {
public:
    static constexpr size_t BUFFER_SIZE = 32;

    SmallString();
    explicit SmallString(const char* str);
    SmallString(const SmallString& other);
    SmallString& operator=(const SmallString& other);
    ~SmallString();

    void assign(const char* str);
    void assign(const char* str, size_t len);
    void append(const char* str);
    void append(const char* str, size_t len);

    const char* data() const;
    const char* c_str() const;
    size_t size() const;
    size_t length() const;
    size_t capacity() const;
    bool empty() const;

private:
    void ensure_capacity(size_t needed);
    void release();

    union {
        struct {
            char* m_data;
            size_t m_capacity;
        } m_heap;
        char m_local[BUFFER_SIZE];
    };
    size_t m_size;
    bool m_using_sso;
};
