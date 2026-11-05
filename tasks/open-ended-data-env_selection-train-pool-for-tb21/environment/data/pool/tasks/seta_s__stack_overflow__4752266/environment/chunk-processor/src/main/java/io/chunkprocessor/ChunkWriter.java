package io.chunkprocessor;

import java.io.*;

public class ChunkWriter {
    public void write(byte[] data, File output) throws IOException {
        FileOutputStream fos = new FileOutputStream(output);
        BufferedOutputStream bos = new BufferedOutputStream(fos);
        bos.write(data);
        fos.close();
        bos.close();
    }
}
