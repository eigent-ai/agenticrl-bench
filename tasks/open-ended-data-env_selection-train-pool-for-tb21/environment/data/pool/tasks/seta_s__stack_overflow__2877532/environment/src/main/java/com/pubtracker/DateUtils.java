package com.pubtracker;

import java.util.Date;
import java.text.SimpleDateFormat;

public class DateUtils {

    @SuppressWarnings("deprecation")
    public static Date createDate(int year, int month, int day) {
        return new Date(year, month, day);
    }

    public static String formatDate(Date date, String pattern) {
        SimpleDateFormat sdf = new SimpleDateFormat(pattern);
        return sdf.format(date);
    }
}
