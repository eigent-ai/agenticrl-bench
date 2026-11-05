package com.app;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.logging.Logger;

/**
 * Handles image file processing and metadata extraction.
 */
public class ImageProcessor {
    private static final Logger logger = Logger.getLogger(ImageProcessor.class.getName());
    private static final long MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

    public void process(File file) {
        if (!file.exists()) {
            logger.warning("File not found: " + file.getAbsolutePath());
            return;
        }

        if (file.length() > MAX_FILE_SIZE) {
            logger.warning("File too large, skipping: " + file.getName());
            return;
        }

        String filename = file.getName().toLowerCase();
        if (filename.endsWith(".png") || filename.endsWith(".jpg")) {
            processImage(file);
        }
    }

    private void processImage(File file) {
        try {
            byte[] data = Files.readAllBytes(file.toPath());
            logger.info("Processed image: " + file.getName() + " (" + data.length + " bytes)");
        } catch (IOException e) {
            logger.severe("Failed to read image: " + e.getMessage());
        }
    }
}
