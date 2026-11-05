public class StudentRecord {
    private final String name;
    private final String subject;
    private final String department;
    private final int mark1;
    private final int mark2;
    private final int mark3;

    public StudentRecord(String name, String subject, String department,
                         int mark1, int mark2, int mark3) {
        this.name = name;
        this.subject = subject;
        this.department = department;
        this.mark1 = mark1;
        this.mark2 = mark2;
        this.mark3 = mark3;
    }

    public String getName()       { return name; }
    public String getSubject()    { return subject; }
    public String getDepartment() { return department; }
    public int getMark1()         { return mark1; }
    public int getMark2()         { return mark2; }
    public int getMark3()         { return mark3; }
    public int getTotalScore()    { return mark1 + mark2 + mark3; }
}
