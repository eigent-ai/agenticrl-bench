package com.pubtracker;

import java.util.Calendar;
import java.util.Date;

public class TimeSlotManager {

    public static Date setPublishTime(Date date, int hour, int minute) {
        Calendar cal = Calendar.getInstance();
        cal.setTime(date);
        cal.set(Calendar.HOUR_OF_DAY, hour);
        cal.set(Calendar.MINUTE, minute);
        return cal.getTime();
    }
}
