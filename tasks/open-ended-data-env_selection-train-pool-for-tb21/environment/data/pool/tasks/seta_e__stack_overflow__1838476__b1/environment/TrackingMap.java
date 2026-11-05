package com.ingester;

import java.util.HashMap;

public class TrackingMap extends HashMap<String, Element> {
    private int duplicateCount = 0;

    @Override
    public Element put(String key, Element value) {
        if (containsKey(key)) {
            duplicateCount++;
        }
        return super.put(key, value);
    }

    public int getDuplicateCount() {
        return duplicateCount;
    }
}
