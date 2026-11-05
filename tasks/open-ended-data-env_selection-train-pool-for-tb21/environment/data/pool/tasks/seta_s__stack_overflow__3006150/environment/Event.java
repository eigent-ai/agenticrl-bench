package com.reports;

import java.util.Date;

public class Event {
    private String id;
    private Date timestamp;
    private String source;
    private String category;
    private String originalTimestamp;

    public Event(String id, Date timestamp, String source, String originalTimestamp) {
        this.id = id;
        this.timestamp = timestamp;
        this.source = source;
        this.originalTimestamp = originalTimestamp;
    }

    public String getId() { return id; }
    public Date getTimestamp() { return timestamp; }
    public String getSource() { return source; }
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
    public String getOriginalTimestamp() { return originalTimestamp; }
}
