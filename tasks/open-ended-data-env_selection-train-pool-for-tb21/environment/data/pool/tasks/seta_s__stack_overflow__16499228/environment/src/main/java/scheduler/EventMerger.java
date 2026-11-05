package scheduler;

import java.util.Calendar;
import java.util.TimeZone;

public class EventMerger {

    public static Calendar mergeDateAndTime(Calendar dateCal, int hour, int minute) {
        Calendar merged = Calendar.getInstance(TimeZone.getTimeZone("UTC"));
        merged.set(Calendar.YEAR, dateCal.get(Calendar.YEAR));
        merged.set(Calendar.MONTH, dateCal.get(Calendar.MONTH));
        merged.set(Calendar.DAY_OF_MONTH, dateCal.get(Calendar.DAY_OF_MONTH));
        merged.set(Calendar.HOUR_OF_DAY, hour);
        merged.set(Calendar.MINUTE, minute);
        return merged;
    }
}
