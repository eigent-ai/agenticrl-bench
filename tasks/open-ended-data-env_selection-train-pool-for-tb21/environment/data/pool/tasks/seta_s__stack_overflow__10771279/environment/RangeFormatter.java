import java.text.SimpleDateFormat;
import java.util.*;

public class RangeFormatter {

    public static String formatRange(Calendar cal, String startTime, String endTime) {
        String[] startParts = startTime.split(":");
        int startHour = Integer.parseInt(startParts[0]);
        int startMinute = Integer.parseInt(startParts[1]);

        cal.set(Calendar.HOUR_OF_DAY, startHour);
        cal.set(Calendar.MINUTE, startMinute);

        SimpleDateFormat fullFormat = new SimpleDateFormat("EEEE, MMMM d, yyyy KK:mm a");
        String startStr = fullFormat.format(cal.getTime());

        String[] endParts = endTime.split(":");
        int endHour = Integer.parseInt(endParts[0]);
        int endMinute = Integer.parseInt(endParts[1]);

        cal.set(Calendar.HOUR_OF_DAY, endHour);
        cal.set(Calendar.MINUTE, endMinute);

        SimpleDateFormat endFormat = new SimpleDateFormat("EEEE, MMMM d, yyyy KK:mm a");
        String endStr = endFormat.format(cal.getTime());

        return startStr + " - " + endStr;
    }
}
