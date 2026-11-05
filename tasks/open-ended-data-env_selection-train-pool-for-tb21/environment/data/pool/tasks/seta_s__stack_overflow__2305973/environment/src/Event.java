import java.util.Date;

public class Event {
    private long id;
    private String name;
    private Date timestamp;

    public Event() {}

    public Event(String name, Date timestamp) {
        this.name = name;
        this.timestamp = timestamp;
    }

    public long getId() { return id; }
    public void setId(long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public Date getTimestamp() { return timestamp; }
    public void setTimestamp(Date timestamp) { this.timestamp = timestamp; }
}
