package com.example.core;

import com.example.utils.StringHelper;

public class DataProcessor {
    private String prefix;

    public DataProcessor(String prefix) {
        this.prefix = prefix;
    }

    public String process(String data) {
        return StringHelper.format(prefix, data);
    }
}
