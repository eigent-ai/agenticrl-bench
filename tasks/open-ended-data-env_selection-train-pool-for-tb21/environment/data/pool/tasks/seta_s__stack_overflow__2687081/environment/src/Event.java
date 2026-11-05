import java.util.Date;

public class Event {
    private String name;
    private String dateStr;
    private Date date;
    private String category;

    public Event(String name, String dateStr, Date date, String category) {
        this.name = name;
        this.dateStr = dateStr;
        this.date = date;
        this.category = category;
    }

    public String getName() { return name; }
    public String getDateStr() { return dateStr; }
    public Date getDate() { return date; }
    public String getCategory() { return category; }
}
