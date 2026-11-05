import java.util.Calendar;

public class Task {
    private String name;
    private String description;
    private Calendar lastExecuted;
    private Calendar nextExecution;

    public Task(String name, String description, Calendar lastExecuted) {
        this.name = name;
        this.description = description;
        this.lastExecuted = lastExecuted;
    }

    public String getName() { return name; }
    public String getDescription() { return description; }
    public Calendar getLastExecuted() { return lastExecuted; }
    public Calendar getNextExecution() { return nextExecution; }

    public void setNextExecution(Calendar nextExecution) {
        this.nextExecution = nextExecution;
    }
}
