import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class EventFilter {

    public static List<Event> filterByRange(List<Event> events, Date start, Date end) {
        List<Event> filtered = new ArrayList<>();
        for (Event e : events) {
            if ((!DateHelper.isBefore(e.getDate(), start)) &&
                (!DateHelper.isAfter(e.getDate(), end))) {
                filtered.add(e);
            }
        }
        return filtered;
    }

    public static int getMonth(Date d) {
        return d.getMonth();
    }

    public static int getDay(Date d) {
        return d.getDate();
    }
}
