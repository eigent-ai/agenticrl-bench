package com.scheduler;

import java.util.Calendar;
import java.util.TimeZone;

public class TimeZoneResolver {

    public String detectSystemTimezone() {
        Calendar cal = Calendar.getInstance();
        int rawOffset = cal.get(Calendar.ZONE_OFFSET);

        String[] availableIds = TimeZone.getAvailableIDs();
        String detectedZone = "UTC";

        for (String id : availableIds) {
            TimeZone tz = TimeZone.getTimeZone(id);
            if (tz.getRawOffset() == rawOffset) {
                detectedZone = id;
                break;
            }
        }

        System.out.println("Detected system timezone: " + detectedZone);
        return detectedZone;
    }
}
