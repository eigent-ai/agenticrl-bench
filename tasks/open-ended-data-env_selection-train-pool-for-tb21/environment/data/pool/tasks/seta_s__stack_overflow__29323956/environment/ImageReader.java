package contrast;

import java.io.*;

public class ImageReader {
    private int width;
    private int height;
    private double[][] pixels;

    public ImageReader(String path) throws IOException {
        try (DataInputStream dis = new DataInputStream(
                new BufferedInputStream(new FileInputStream(path)))) {
            String magic = readLine(dis);
            if (!magic.equals("P5")) {
                throw new IOException("Not a P5 PGM file: " + magic);
            }
            String line = readLine(dis);
            while (line.startsWith("#")) {
                line = readLine(dis);
            }
            String[] dims = line.trim().split("\\s+");
            width = Integer.parseInt(dims[0]);
            height = Integer.parseInt(dims[1]);
            String maxValStr = readLine(dis);
            int maxVal = Integer.parseInt(maxValStr.trim());

            pixels = new double[width][height];
            for (int y = 0; y < height; y++) {
                for (int x = 0; x < width; x++) {
                    int raw = dis.readUnsignedByte();
                    pixels[x][y] = (double) raw;
                }
            }
        }
    }

    private String readLine(DataInputStream dis) throws IOException {
        StringBuilder sb = new StringBuilder();
        int c;
        while ((c = dis.read()) != -1 && c != '\n') {
            sb.append((char) c);
        }
        return sb.toString().trim();
    }

    public int getWidth() { return width; }
    public int getHeight() { return height; }
    public double[][] getPixels() { return pixels; }
}
