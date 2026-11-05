package com.warehouse;

public interface CacheManagerMBean {
    int getCacheSize();
    double getHitRate();
    void rotateCache();
    boolean clearEntry(String key);
}
