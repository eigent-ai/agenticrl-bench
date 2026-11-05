import java.io.File;

public class DirectoryUtils {

    public static void ensureDirectory(File dir) {
        if (!dir.exists()) {
            dir.mkdir();
        }
    }
}
