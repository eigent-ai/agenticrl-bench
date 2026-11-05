package com.resourceapp;

import java.io.InputStream;
import java.util.Properties;

public class ConfigLoader {
    private Properties props = new Properties();

    public boolean load() {
        System.out.println("[ConfigLoader] Attempting to load resource: /config.properties");
        try {
            InputStream is = props.getClass().getResourceAsStream("/config.properties");
            if (is == null) {
                System.out.println("[ConfigLoader] Resource stream is null - failed to locate resource");
                return false;
            }
            props.load(is);
            is.close();
            System.out.println("[ConfigLoader] Loaded app.name=" + props.getProperty("app.name"));
            return true;
        } catch (Exception e) {
            System.out.println("[ConfigLoader] Exception: " + e.getMessage());
            return false;
        }
    }
}
