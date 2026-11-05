import java.util.*;

public class DateBuilder {

    public static Date buildDate(int year, int month, int day,
                                  int hour, int minute, int second,
                                  String timezone) {
        Calendar cal = Calendar.getInstance(TimeZone.getTimeZone(timezone));
        cal.set(Calendar.YEAR, year);
        cal.set(Calendar.MONTH, month);
        cal.set(Calendar.DAY_OF_MONTH, day);
        cal.set(Calendar.HOUR_OF_DAY, hour);
        cal.set(Calendar.MINUTE, minute);
        cal.set(Calendar.SECOND, second);
        cal.set(Calendar.MILLISECOND, 0);
        return cal.getTime();
    }
}
