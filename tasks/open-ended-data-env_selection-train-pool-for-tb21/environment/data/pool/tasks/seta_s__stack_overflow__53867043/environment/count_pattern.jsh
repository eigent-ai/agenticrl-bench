//usr/bin/env jshell "$0" "$@"; exit $?
import java.nio.file.*;
import java.util.*;
import java.util.stream.*;

{
    String logFile = System.getProperty("logFile");
    String pattern = System.getenv("SEARCH_PATTERN");
    if (logFile == null || pattern == null) {
        System.err.println("Error: logFile property or SEARCH_PATTERN env var not set");
        System.exit(1);
    }
    List<String> lines = Files.readAllLines(Path.of(logFile));
    long count = lines.stream().filter(l -> l.contains(pattern)).count();
    System.out.println("Lines matching '" + pattern + "': " + count);
}
/exit
