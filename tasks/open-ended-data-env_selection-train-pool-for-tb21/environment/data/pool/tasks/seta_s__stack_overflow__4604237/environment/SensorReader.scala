package pipeline

import scala.io.Source

case class SensorReading(id: Int, name: String, location: String, value: Double, timestamp: String)

object SensorReader {
  def read(path: String): Seq[SensorReading] = {
    val source = Source.fromFile(path)("UTF-8")
    try {
      source.getLines().drop(1).map { line =>
        val parts = line.split(",", -1)
        SensorReading(
          parts(0).trim.toInt,
          parts(1).trim,
          parts(2).trim,
          parts(3).trim.toDouble,
          parts(4).trim
        )
      }.toList
    } finally {
      source.close()
    }
  }
}
