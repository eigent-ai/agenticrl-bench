package com.util;

import java.util.ArrayList;
import java.util.List;

public class ConnectionPool {
    private final int maxSize;
    private final List<Object> connections = new ArrayList<>();

    public ConnectionPool(int maxSize) {
        this.maxSize = maxSize;
    }

    public int available() {
        return maxSize - connections.size();
    }
}
