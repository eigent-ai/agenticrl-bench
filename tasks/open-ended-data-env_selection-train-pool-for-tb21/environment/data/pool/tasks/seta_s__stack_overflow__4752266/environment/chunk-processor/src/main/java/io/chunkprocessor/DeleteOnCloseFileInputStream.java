package io.chunkprocessor;

import java.io.*;

public class DeleteOnCloseFileInputStream extends FileInputStream {
    private String fileName;

    public DeleteOnCloseFileInputStream(String path) throws FileNotFoundException {
        this(new File(path));
    }

    public DeleteOnCloseFileInputStream(File file) throws FileNotFoundException {
        super(file);
        this.fileName = file.getName();
    }

    @Override
    public void close() throws IOException {
        try {
            super.close();
        } finally {
            if (fileName != null) {
                new File(fileName).delete();
                fileName = null;
            }
        }
    }
}
