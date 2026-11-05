package com.fileutil;

import java.io.*;

public class TextNormalizer {
    public static String analyze(String path) throws IOException {
        BufferedReader reader = new BufferedReader(new FileReader(path));
        StringBuilder content = new StringBuilder();
        String line;
        int lineCount = 0;
        while ((line = reader.readLine()) != null) {
            if (lineCount > 0) {
                content.append(System.lineSeparator());
            }
            content.append(line);
            lineCount++;
        }
        reader.close();

        String text = content.toString();
        boolean hasCRLF = text.contains("\r\n");
        boolean hasCR = !hasCRLF && text.contains("\r");
        boolean hasLF = text.contains("\n");

        String endingType;
        if (hasCRLF) {
            endingType = "CRLF";
        } else if (hasCR) {
            endingType = "CR";
        } else if (hasLF) {
            endingType = "LF";
        } else {
            endingType = "NONE";
        }

        return "lines=" + lineCount + ",endings=" + endingType;
    }
}
