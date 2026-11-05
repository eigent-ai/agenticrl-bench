package com.pubtracker;

import java.util.Date;

public class Publication {
    private String title;
    private Date publishDate;
    private String issn;

    public Publication(String title, Date publishDate, String issn) {
        this.title = title;
        this.publishDate = publishDate;
        this.issn = issn;
    }

    public String getTitle() {
        return title;
    }

    public Date getPublishDate() {
        return publishDate;
    }

    public String getIssn() {
        return issn;
    }
}
