import java.util.*;
import java.text.*;

public class WeekReport {
    public static void main(String[] args) throws Exception {
        if (args.length < 1) {
            System.err.println("Usage: java WeekReport <YYYY-MM-DD>");
            System.exit(1);
        }

        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        Date date = sdf.parse(args[0]);

        Calendar cal = Calendar.getInstance(Locale.US);
        cal.setTime(date);

        cal.set(Calendar.DAY_OF_WEEK, Calendar.MONDAY);

        DateFormat fmt = new SimpleDateFormat("yyyy-MM-dd");
        String startDate = fmt.format(cal.getTime());

        cal.add(Calendar.DATE, 5);
        String endDate = fmt.format(cal.getTime());

        System.out.println("Week range for " + args[0] + ":");
        System.out.println("Start: " + startDate);
        System.out.println("End:   " + endDate);
    }
}
