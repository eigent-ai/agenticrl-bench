import java.util.*;
import java.text.*;

public class TimeUtils {

    public static long convertToTargetMillis(long utcMillis, TimeZone sourceTZ, TimeZone targetTZ) {
        int sourceOffset = sourceTZ.getRawOffset();
        int targetOffset = targetTZ.getRawOffset();
        return utcMillis - sourceOffset + targetOffset;
    }

    public static String formatDateTime(Calendar cal, TimeZone targetTZ) {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm");
        return sdf.format(cal.getTime());
    }
}
