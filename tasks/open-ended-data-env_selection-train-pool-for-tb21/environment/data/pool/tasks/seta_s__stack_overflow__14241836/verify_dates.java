import java.util.Calendar;
import java.util.GregorianCalendar;

public class verify_dates {
    public static void main(String[] args) {
        // Test 1: August 1, 2024
        Calendar cal1 = new GregorianCalendar(2024, Calendar.AUGUST, 1);
        int dow1 = cal1.get(Calendar.DAY_OF_WEEK);
        System.out.println("Test 1: August 1, 2024");
        System.out.println("  Day of week: " + dow1 + " (1=SUN, 2=MON, ..., 5=THU, 7=SAT)");
        System.out.println("  Day name: " + getDayName(dow1));

        // Find Sunday before Aug 1, 2024
        Calendar sundayBefore1 = new GregorianCalendar(2024, Calendar.AUGUST, 1);
        int currentDow = sundayBefore1.get(Calendar.DAY_OF_WEEK);
        int daysToSubtract = (currentDow == Calendar.SUNDAY) ? 0 : (currentDow - Calendar.SUNDAY);
        sundayBefore1.add(Calendar.DAY_OF_MONTH, -daysToSubtract);
        System.out.println("  Days to subtract (correct formula): " + daysToSubtract);
        System.out.println("  Sunday before: " + formatDate(sundayBefore1));

        // Show buggy calculation
        Calendar buggy1 = new GregorianCalendar(2024, Calendar.AUGUST, 1);
        buggy1.add(Calendar.DAY_OF_MONTH, -currentDow);
        System.out.println("  Buggy calculation (subtract " + currentDow + "): " + formatDate(buggy1));
        System.out.println();

        // Test 2: February 1, 2025
        Calendar cal2 = new GregorianCalendar(2025, Calendar.FEBRUARY, 1);
        int dow2 = cal2.get(Calendar.DAY_OF_WEEK);
        System.out.println("Test 2: February 1, 2025");
        System.out.println("  Day of week: " + dow2 + " (1=SUN, 2=MON, ..., 5=THU, 7=SAT)");
        System.out.println("  Day name: " + getDayName(dow2));

        // Find Sunday before Feb 1, 2025
        Calendar sundayBefore2 = new GregorianCalendar(2025, Calendar.FEBRUARY, 1);
        currentDow = sundayBefore2.get(Calendar.DAY_OF_WEEK);
        daysToSubtract = (currentDow == Calendar.SUNDAY) ? 0 : (currentDow - Calendar.SUNDAY);
        sundayBefore2.add(Calendar.DAY_OF_MONTH, -daysToSubtract);
        System.out.println("  Days to subtract (correct formula): " + daysToSubtract);
        System.out.println("  Sunday before: " + formatDate(sundayBefore2));

        // Show buggy calculation
        Calendar buggy2 = new GregorianCalendar(2025, Calendar.FEBRUARY, 1);
        buggy2.add(Calendar.DAY_OF_MONTH, -currentDow);
        System.out.println("  Buggy calculation (subtract " + currentDow + "): " + formatDate(buggy2));
        System.out.println();

        // Test 3: Verify Jan 1, 2024 and Jan 1, 2025
        Calendar jan2024 = new GregorianCalendar(2024, Calendar.JANUARY, 1);
        System.out.println("Test 3: Verification of base dates");
        System.out.println("  Jan 1, 2024: " + getDayName(jan2024.get(Calendar.DAY_OF_WEEK)));

        Calendar jan2025 = new GregorianCalendar(2025, Calendar.JANUARY, 1);
        System.out.println("  Jan 1, 2025: " + getDayName(jan2025.get(Calendar.DAY_OF_WEEK)));
        System.out.println();

        // Test 4: August 2024 grid
        System.out.println("Test 4: August 2024 grid (starting from Sunday)");
        Calendar gridStart = new GregorianCalendar(2024, Calendar.AUGUST, 1);
        int dow = gridStart.get(Calendar.DAY_OF_WEEK);
        int daysBack = (dow == Calendar.SUNDAY) ? 0 : (dow - Calendar.SUNDAY);
        gridStart.add(Calendar.DAY_OF_MONTH, -daysBack);

        System.out.println("  Grid starts at: " + formatDate(gridStart));
        System.out.println("  Grid layout (dates[index]):");
        for (int week = 0; week < 6; week++) {
            System.out.print("  Week " + week + ": ");
            for (int day = 0; day < 7; day++) {
                int index = week * 7 + day;
                System.out.print(String.format("%2d ", gridStart.get(Calendar.DAY_OF_MONTH)));
                gridStart.add(Calendar.DAY_OF_MONTH, 1);
            }
            System.out.println();
        }
    }

    static String getDayName(int dow) {
        String[] names = {"", "SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"};
        return names[dow];
    }

    static String formatDate(Calendar cal) {
        return String.format("%s, %s %d, %d",
            getDayName(cal.get(Calendar.DAY_OF_WEEK)),
            getMonthName(cal.get(Calendar.MONTH)),
            cal.get(Calendar.DAY_OF_MONTH),
            cal.get(Calendar.YEAR));
    }

    static String getMonthName(int month) {
        String[] names = {"January", "February", "March", "April", "May", "June",
                         "July", "August", "September", "October", "November", "December"};
        return names[month];
    }
}
