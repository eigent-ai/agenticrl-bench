package com.example.services;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ServiceC {
    private static final Logger logger = LoggerFactory.getLogger(ServiceC.class);

    public void start() {
        logger.info("Service {} starting on port {}", "ServiceC", 8080);
    }

    public void process(String item) {
        logger.debug("Processing item {}", item);
    }

    public void stop() {
        logger.info("Service stopped");
    }
}
