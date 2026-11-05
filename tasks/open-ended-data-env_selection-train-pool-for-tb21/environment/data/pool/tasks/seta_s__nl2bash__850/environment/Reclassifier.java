package com.app;

import java.io.File;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.Logger;

/**
 * Reclassifies files based on content analysis and heuristics.
 * Used to organize project files into appropriate categories.
 */
public class Reclassifier {
    private static final Logger logger = Logger.getLogger(Reclassifier.class.getName());

    private final Map<String, String> categoryMap;

    public Reclassifier() {
        categoryMap = new HashMap<>();
        categoryMap.put(".java", "source");
        categoryMap.put(".py", "source");
        categoryMap.put(".md", "documentation");
        categoryMap.put(".yaml", "configuration");
        categoryMap.put(".html", "template");
        categoryMap.put(".sh", "script");
    }

    public String classify(File file) {
        String name = file.getName();
        for (Map.Entry<String, String> entry : categoryMap.entrySet()) {
            if (name.endsWith(entry.getKey())) {
                logger.fine("Classified " + name + " as " + entry.getValue());
                return entry.getValue();
            }
        }
        return "unknown";
    }

    public Map<String, Integer> summarize(File[] files) {
        Map<String, Integer> summary = new HashMap<>();
        for (File file : files) {
            String category = classify(file);
            summary.merge(category, 1, Integer::sum);
        }
        return summary;
    }
}
