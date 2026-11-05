package weekdaygen;

import java.io.*;

public class ReportWriter {

    public void write(String path, String content) throws IOException {
        FileWriter fw = new FileWriter(path);
        fw.write(content);
        fw.close();
    }
}
