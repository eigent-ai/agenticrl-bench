package com.fileutil;

import java.io.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;

public class LineSplitter {
    public static int countLines(String path) throws IOException {
        String content = new String(Files.readAllBytes(Paths.get(path)), StandardCharsets.UTF_8);
        if (content.isEmpty()) return 0;
        String[] lines = content.split("\n");
        return lines.length;
    }
}
