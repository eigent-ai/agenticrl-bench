"use strict";

var defaultConfig = {
  port: 3000,
  host: "0.0.0.0",
  apiBaseUrl: "https://api.example.com/v2",
  maxRequestSize: "10mb",
  cors: {
    origin: "*",
    methods: ["GET", "POST", "PUT", "DELETE"],
    allowedHeaders: ["Content-Type", "Authorization"]
  },
  logging: {
    level: "info",
    format: "json",
    destination: "stdout"
  },
  cache: {
    enabled: true,
    ttl: 300,
    maxSize: 1000
  }
};

var envOverrides = {};

function getPublicConfig() {
  return {
    port: getConfig().port,
    host: getConfig().host,
    cors: getConfig().cors,
    logging: { level: getConfig().logging.level }
  };
}

function getConfig() {
  return Object.assign({}, defaultConfig, envOverrides);
}

function getApiBaseUrl() {
  return getConfig().apiBaseUrl;
}

function setOverride(key, value) {
  envOverrides[key] = value;
}

function resetOverrides() {
  envOverrides = {};
}

module.exports = { getPublicConfig, getConfig, getApiBaseUrl, setOverride, resetOverrides };
