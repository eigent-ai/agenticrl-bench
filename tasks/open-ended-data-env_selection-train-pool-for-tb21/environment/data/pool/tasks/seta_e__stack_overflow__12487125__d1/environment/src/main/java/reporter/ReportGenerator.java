package reporter;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;

public class ReportGenerator {

    public static class EventRecord {
        public int id;
        public String utcTimestamp;
        public String localTimestamp;
        public String timezone;
        public String offset;

        public EventRecord(int id, String utcTimestamp, String localTimestamp, String timezone, String offset) {
            this.id = id;
            this.utcTimestamp = utcTimestamp;
            this.localTimestamp = localTimestamp;
            this.timezone = timezone;
            this.offset = offset;
        }
    }

    public void writeReport(List<EventRecord> records, String outputPath) throws IOException {
        try (PrintWriter pw = new PrintWriter(new FileWriter(outputPath))) {
            pw.printf("%-9s| %-28s| %-28s| %-20s| %s%n",
                "Event ID", "UTC Timestamp", "Local Timestamp", "Timezone", "Offset");
            for (EventRecord rec : records) {
                pw.printf("%-9s| %-28s| %-28s| %-20s| %s%n",
                    rec.id, rec.utcTimestamp, rec.localTimestamp, rec.timezone, rec.offset);
            }
        }
    }
}
