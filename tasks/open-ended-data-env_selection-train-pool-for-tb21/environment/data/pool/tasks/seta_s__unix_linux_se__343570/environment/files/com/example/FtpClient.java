package com.example;

public class FtpClient {
    private String host;
    private int port;

    public FtpClient(String host, int port) {
        // TODO: add input validation
        this.host = host;
        this.port = port;
    }

    public void connect() {
        System.out.println("Connecting to " + host + ":" + port);
    }

    public void upload(String path) {
        // TODO: implement retry logic
        System.out.println("Uploading: " + path);
    }
}
