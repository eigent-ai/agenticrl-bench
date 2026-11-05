public class SeverityMapper {

    public static int mapSeverity(String name) {
        if (name == null) return 0;
        switch (name.toUpperCase().trim()) {
            case "DEBUG": return 1;
            case "INFO":  return 2;
            case "WARN":  return 3;
            case "ERROR": return 4;
            case "FATAL": return 5;
            default:      return 0;
        }
    }

    public static String nameForLevel(int level) {
        switch (level) {
            case 1: return "DEBUG";
            case 2: return "INFO";
            case 3: return "WARN";
            case 4: return "ERROR";
            case 5: return "FATAL";
            default: return "UNKNOWN";
        }
    }
}
