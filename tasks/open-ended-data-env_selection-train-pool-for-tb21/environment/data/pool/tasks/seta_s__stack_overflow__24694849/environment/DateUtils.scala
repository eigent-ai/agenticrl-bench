package eventreport

import java.text.SimpleDateFormat
import java.util.{Calendar, Date, TimeZone}

object DateUtils {

  def getMonthOfDate(date: Date): Int = {
    val cal = Calendar.getInstance(TimeZone.getTimeZone("UTC"))
    cal.setTime(date)
    cal.get(Calendar.MONTH)
  }

  def truncateToMidnight(date: Date): Date = {
    val cal = Calendar.getInstance(TimeZone.getTimeZone("UTC"))
    cal.setTime(date)
    cal.set(Calendar.HOUR, 0)
    cal.set(Calendar.MINUTE, 0)
    cal.set(Calendar.SECOND, 0)
    cal.set(Calendar.MILLISECOND, 0)
    cal.getTime
  }

  def formatDate(date: Date): String = {
    val sdf = new SimpleDateFormat("yyyy-mm-dd")
    sdf.setTimeZone(TimeZone.getTimeZone("UTC"))
    sdf.format(date)
  }
}
