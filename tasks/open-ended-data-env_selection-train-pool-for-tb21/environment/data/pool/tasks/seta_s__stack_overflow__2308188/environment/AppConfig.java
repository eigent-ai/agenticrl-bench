package com.example;

import java.io.Serializable;

public class AppConfig implements Serializable {
    private static final long serialVersionUID = 1L;

    private int maxConnections;
    private int timeout;
    private String environment;

    public AppConfig() {}

    public AppConfig(int maxConnections, int timeout, String environment) {
        this.maxConnections = maxConnections;
        this.timeout = timeout;
        this.environment = environment;
    }

    public int getMaxConnections() { return maxConnections; }
    public int getTimeout()        { return timeout; }
    public String getEnvironment() { return environment; }
}
