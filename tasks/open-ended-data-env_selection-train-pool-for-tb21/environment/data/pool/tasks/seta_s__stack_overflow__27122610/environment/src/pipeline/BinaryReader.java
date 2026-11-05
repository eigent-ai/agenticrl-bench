package pipeline;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class BinaryReader {

    public byte[] readFile(String path) throws IOException {
        return Files.readAllBytes(Path.of(path));
    }
}
