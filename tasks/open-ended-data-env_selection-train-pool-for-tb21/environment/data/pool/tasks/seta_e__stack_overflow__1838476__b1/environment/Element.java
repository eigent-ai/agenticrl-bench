package com.ingester;

public class Element {
    private final String uuid;
    private final String name;

    public Element(String uuid, String name) {
        this.uuid = uuid;
        this.name = name;
    }

    public String getUuid() { return uuid; }
    public String getName() { return name; }
}
