package pipeline;

import java.io.File;
import java.io.IOException;

public class Main {

    public static void main(String[] args) {
        if (args.length != 2) {
            System.err.println("Usage: java pipeline.Main <input-dir> <output-dir>");
            System.exit(1);
        }

        String inputDir = args[0];
        String outputDir = args[1];

        File outDir = new File(outputDir);
        if (!outDir.exists()) {
            outDir.mkdirs();
        }

        BinaryReader reader = new BinaryReader();
        BitFieldParser parser = new BitFieldParser();

        File inDir = new File(inputDir);
        File[] binFiles = inDir.listFiles((dir, name) -> name.endsWith(".bin"));

        if (binFiles == null || binFiles.length == 0) {
            System.err.println("No .bin files found in " + inputDir);
            System.exit(1);
        }

        int failures = 0;
        for (File binFile : binFiles) {
            String baseName = binFile.getName().replace(".bin", "");
            String outputPath = outputDir + "/" + baseName + ".csv";

            try {
                System.out.println("Processing " + binFile.getName() + "...");

                byte[] data = reader.readFile(binFile.getAbsolutePath());

                RecordCounter counter = new RecordCounter();
                counter.count(data);
                int numRecords = counter.getRecordCount();

                java.util.List<SensorRecord> records = parser.parse(data, numRecords);

                Aggregator agg = new Aggregator();
                agg.aggregate(records);

                ReportWriter writer = new ReportWriter();
                writer.write(outputPath, records, numRecords, agg.getSum(), agg.getAverage());

                System.out.println("  -> " + outputPath + " (" + numRecords + " records)");
            } catch (IOException e) {
                System.err.println("Error processing " + binFile.getName() + ": " + e.getMessage());
                failures++;
            }
        }

        if (failures > 0) {
            System.err.println(failures + " file(s) failed to process.");
            System.exit(1);
        }

        System.out.println("Pipeline complete.");
    }
}
