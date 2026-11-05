package com.warehouse;

import java.io.File;
import java.io.IOException;

public class CacheManager implements CacheManagerMBean {
    private int cacheSize = 4096;
    private double hitRate = 0.87;

    public int getCacheSize() {
        return cacheSize;
    }

    public double getHitRate() {
        return hitRate;
    }

    public void rotateCache() {
        cacheSize = 0;
        try {
            new File("/tmp/cache_rotated").createNewFile();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public boolean clearEntry(String key) {
        if (key != null && !key.isEmpty()) {
            cacheSize = Math.max(0, cacheSize - 1);
            return true;
        }
        return false;
    }
}
