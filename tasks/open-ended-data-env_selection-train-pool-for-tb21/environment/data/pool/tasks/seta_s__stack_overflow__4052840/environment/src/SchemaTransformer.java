import java.io.*;
import java.nio.file.*;

/**
 * Reads one field name per line from an input file, converts each name to
 * camelCase by lower-casing the first character, and writes the results to an
 * output file (one per line, preserving order).
 */
public class SchemaTransformer {

    public static void main(String[] args) throws IOException {
        if (args.length != 2) {
            System.err.println("Usage: SchemaTransformer <input-file> <output-file>");
            System.exit(1);
        }

        Path inputPath  = Paths.get(args[0]);
        Path outputPath = Paths.get(args[1]);

        if (outputPath.getParent() != null) {
            Files.createDirectories(outputPath.getParent());
        }

        try (BufferedReader reader = Files.newBufferedReader(inputPath);
             PrintWriter    writer = new PrintWriter(Files.newBufferedWriter(outputPath))) {

            String line;
            while ((line = reader.readLine()) != null) {
                writer.println(StringNormalizer.decapitalize(line));
            }
        }
    }
}
