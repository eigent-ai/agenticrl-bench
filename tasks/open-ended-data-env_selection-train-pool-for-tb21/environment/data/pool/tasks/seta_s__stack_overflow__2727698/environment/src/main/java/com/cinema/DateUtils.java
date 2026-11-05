package com.cinema;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.TimeZone;

public class DateUtils {

    private static final SimpleDateFormat FORMAT = new SimpleDateFormat("yyyy-MM-dd HH:mm");

    static {
        FORMAT.setTimeZone(TimeZone.getDefault());
    }

    public static Date createDate(int year, int month, int day, int hour, int minute) {
        Calendar calendar = Calendar.getInstance();
        calendar.clear();
        calendar.set(year, month, day, hour, minute, 0);
        return calendar.getTime();
    }

    public static String formatDate(Date date) {
        synchronized (FORMAT) {
            return FORMAT.format(date);
        }
    }
}
