package com.library;

import java.util.TimeZone;

public class AppConfig {
    static {
        TimeZone.setDefault(TimeZone.getTimeZone("America/New_York"));
    }

    public static final double DAILY_LATE_FEE = 0.25;
    public static final int DEFAULT_LOAN_DAYS = 14;

    public static void init() {
        // triggers static initializer
    }
}
