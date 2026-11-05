package com.example;

import java.io.File;
import java.io.IOException;

public class TempWorkspace {
    private File rootDir;

    public void initWorkspace(String prefix) throws IOException {
        File temp = File.createTempFile(prefix, Long.toString(System.nanoTime()));
        if (!temp.mkdir()) {
            throw new IOException("Could not create temp directory: " + temp.getAbsolutePath());
        }
        rootDir = temp;
    }

    public File createStageDir(String relativePath) throws IOException {
        if (rootDir == null) {
            throw new IllegalStateException("Workspace not initialized");
        }
        File stageDir = new File(rootDir, relativePath);
        if (!stageDir.mkdir()) {
            throw new IOException("Could not create stage directory: " + relativePath);
        }
        return stageDir;
    }

    public void cleanup() throws IOException {
        if (rootDir != null && rootDir.exists()) {
            if (!rootDir.delete()) {
                throw new IOException("Could not delete workspace: " + rootDir.getAbsolutePath());
            }
            rootDir = null;
        }
    }

    public File getRootDir() { return rootDir; }
    public String getRootPath() { return rootDir != null ? rootDir.getAbsolutePath() : ""; }
}
