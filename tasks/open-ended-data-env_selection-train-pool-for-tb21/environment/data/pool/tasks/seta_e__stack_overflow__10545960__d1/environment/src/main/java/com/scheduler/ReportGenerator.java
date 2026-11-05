package com.scheduler;

import java.io.FileWriter;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.List;

public class ReportGenerator {

    public String formatTimestamp(Calendar cal) {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss z");
        return sdf.format(cal.getTime());
    }

    public void writeReport(List<String[]> results, String outputPath) throws Exception {
        try (PrintWriter pw = new PrintWriter(new FileWriter(outputPath))) {
            pw.println("event_name,source_city,utc_timestamp,target_city,converted_time");
            for (String[] row : results) {
                pw.println(String.join(",", row));
            }
        }
    }
}
