package com.ingester;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class CsvParser {
    public static List<Element> parse(String filePath) {
        List<Element> elements = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String header = reader.readLine(); // skip header
            if (header == null) return elements;

            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(",", 2);
                if (parts.length < 2) continue;
                String uuid = parts[0].trim();
                String name = parts[1].trim();
                if (!uuid.isEmpty()) {
                    elements.add(new Element(uuid, name));
                }
            }
        } catch (IOException e) {
            System.err.println("Error reading " + filePath + ": " + e.getMessage());
        }
        return elements;
    }
}
