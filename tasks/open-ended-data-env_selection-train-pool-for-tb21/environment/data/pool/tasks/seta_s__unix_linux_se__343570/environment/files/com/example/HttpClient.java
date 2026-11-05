package com.example;

public class HttpClient {
    private String baseUrl;

    public HttpClient(String baseUrl) {
        this.baseUrl = baseUrl;
    }

    public String get(String endpoint) {
        return "GET " + baseUrl + endpoint;
    }
}
