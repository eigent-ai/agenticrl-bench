import java.util.Date;

public class DateHelper {

    public static Date createDate(int year, int month, int day) {
        return new Date(year, month, day);
    }

    public static Date parseDate(String dateStr) {
        String[] parts = dateStr.split("-");
        int year = Integer.parseInt(parts[0]);
        int month = Integer.parseInt(parts[1]);
        int day = Integer.parseInt(parts[2]);
        return createDate(year, month, day);
    }

    public static boolean isAfter(Date a, Date b) {
        return a.getTime() > b.getTime();
    }

    public static boolean isBefore(Date a, Date b) {
        return a.getTime() < b.getTime();
    }

    public static String formatDate(Date d) {
        return String.format("%04d-%02d-%02d",
            d.getYear() + 1900,
            d.getMonth() + 1,
            d.getDate());
    }
}
