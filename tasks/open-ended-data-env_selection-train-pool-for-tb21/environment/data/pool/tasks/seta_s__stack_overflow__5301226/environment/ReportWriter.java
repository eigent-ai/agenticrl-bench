import java.io.*;
import java.text.SimpleDateFormat;
import java.util.*;

public class ReportWriter {

    private static SimpleDateFormat outputFormat;
    private static SimpleDateFormat yearMonthFormat;

    static {
        outputFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        yearMonthFormat = new SimpleDateFormat("yyyyMM");
    }

    public static String formatDate(Date date) {
        return outputFormat.format(date);
    }

    public static String formatYearMonth(Date date) {
        return yearMonthFormat.format(date);
    }

    public static void writeReport(String outputFile, List<String[]> results) {
        try {
            File parent = new File(outputFile).getParentFile();
            if (parent != null && !parent.exists()) {
                parent.mkdirs();
            }
            PrintWriter pw = new PrintWriter(new FileWriter(outputFile));
            pw.println("id,event_name,original_date,normalized_date,year_month");
            for (String[] row : results) {
                pw.println(String.join(",", row));
            }
            pw.close();
        } catch (IOException e) {
            System.err.println("Failed to write output file: " + e.getMessage());
        }
    }
}
