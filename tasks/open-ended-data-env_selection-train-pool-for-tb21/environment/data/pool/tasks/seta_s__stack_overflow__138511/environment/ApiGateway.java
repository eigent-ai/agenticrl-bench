package com.example;

import java.io.*;
import java.text.SimpleDateFormat;
import java.util.Date;

public class ApiGateway {
    public static void main(String[] args) {
        String logDir = "/opt/services/api-gateway/logs";
        new File(logDir).mkdirs();
        String logFile = logDir + "/api-gateway.log";
        System.out.println("ApiGateway starting...");
        try (PrintWriter pw = new PrintWriter(new FileWriter(logFile, true))) {
            while (true) {
                String ts = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());
                String msg = ts + " [ApiGateway] heartbeat - running";
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
