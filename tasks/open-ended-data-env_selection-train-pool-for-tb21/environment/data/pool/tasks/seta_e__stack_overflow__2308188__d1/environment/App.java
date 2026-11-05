package com.example;

import java.io.*;
import java.util.Properties;

public class App {
    public static void main(String[] args) throws Exception {
        // Load text config (classpath)
        Properties props = new Properties();
        try (InputStream is = App.class.getResourceAsStream("/config.properties")) {
            if (is == null) throw new FileNotFoundException("config.properties not found in classpath");
            props.load(is);
        }
        System.out.println("App: " + props.getProperty("app.name") + " v" + props.getProperty("app.version"));

        // Load binary config (classpath)
        try (ObjectInputStream ois = new ObjectInputStream(
                App.class.getResourceAsStream("/data.ser"))) {
            AppConfig config = (AppConfig) ois.readObject();
            System.out.println("Max connections: " + config.getMaxConnections());
            System.out.println("Timeout: "         + config.getTimeout());
            System.out.println("Environment: "     + config.getEnvironment());
        }
        System.out.println("Application started successfully");
    }
}
