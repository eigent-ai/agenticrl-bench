import java.io.*;
import java.nio.file.*;

public class ReportWriter {

    public static void write(String path, String content) {
        try {
            Files.writeString(Path.of(path), content);
        } catch (IOException e) {
            throw new RuntimeException("Report generation failed");
        }
    }
}
