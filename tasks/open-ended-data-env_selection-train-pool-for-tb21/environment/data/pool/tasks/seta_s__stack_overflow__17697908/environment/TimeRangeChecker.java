package scheduler;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

public class TimeRangeChecker {

    private static final SimpleDateFormat sdf = new SimpleDateFormat("HH:mm:ss");

    public static synchronized boolean isInRange(String time, String start, String end) {
        try {
            Date t = sdf.parse(time);
            Date s = sdf.parse(start);
            Date e = sdf.parse(end);
            return t.after(s) && t.before(e);
        } catch (Exception ex) {
            return false;
        }
    }

    public static synchronized boolean isWithinProximity(String time1, String time2, int minutes) {
        try {
            Date d1 = sdf.parse(time1);
            Date d2 = sdf.parse(time2);
            Calendar c1 = Calendar.getInstance();
            c1.setTime(d1);
            Calendar c2 = Calendar.getInstance();
            c2.setTime(d2);
            int min1 = c1.get(Calendar.MINUTE);
            int min2 = c2.get(Calendar.MINUTE);
            return Math.abs(min1 - min2) <= minutes;
        } catch (Exception ex) {
            return false;
        }
    }
}
