package com.example.util;

import java.util.Properties;

public class ConfigLoader {
    private static final int MAX_CONNECTIONS = 100;
    private static final int DEFAULT_TIMEOUT_MS = 5000;

    public static int getMaxConnections() {
        return MAX_CONNECTIONS;
    }

    public static Properties loadDefaults() {
        String configFile = "/etc/app/config.properties";
        Properties props = new Properties();
        props.setProperty("host", "localhost");
        props.setProperty("port", "8080");
        return props;
    }
}
