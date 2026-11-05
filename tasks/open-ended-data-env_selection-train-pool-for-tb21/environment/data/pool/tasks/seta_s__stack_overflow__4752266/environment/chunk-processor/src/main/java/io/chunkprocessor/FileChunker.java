package io.chunkprocessor;

import java.io.*;

public class FileChunker {
    public void split(File input, File chunkDir, int chunkSize) throws IOException {
        try (FileInputStream fis = new FileInputStream(input)) {
            byte[] buffer = new byte[chunkSize];
            int chunkNum = 0;
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                File chunk = new File(chunkDir, "chunk_" + String.format("%05d", chunkNum) + ".tmp");
                try (FileOutputStream fos = new FileOutputStream(chunk)) {
                    fos.write(buffer);
                }
                chunkNum++;
            }
        }
    }
}
