package com.example;

import java.io.*;
import java.text.SimpleDateFormat;
import java.util.Date;

public class DataProcessor {
    public static void main(String[] args) {
        String logDir = "/opt/services/data-processor/logs";
        new File(logDir).mkdirs();
        String logFile = logDir + "/data-processor.log";
        System.out.println("DataProcessor starting...");
        try (PrintWriter pw = new PrintWriter(new FileWriter(logFile, true))) {
            while (true) {
                String ts = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());
                String msg = ts + " [DataProcessor] heartbeat - running";
                pw.println(msg);
                pw.flush();
                System.out.println(msg);
                Thread.sleep(2000);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
