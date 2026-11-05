package pipeline

import java.io.{BufferedOutputStream, FileOutputStream, InputStream}
import java.nio.ByteBuffer

object BinaryExporter {

  private class ByteStreamAdapter(data: Array[Byte]) extends InputStream {
    private var pos = 0

    override def read(): Int = {
      if (pos < data.length) {
        val b = data(pos)
        pos += 1
        b.toInt
      } else {
        -1
      }
    }
  }

  def export(sensors: Seq[SensorReading], outputPath: String): Unit = {
    val bytes = encodeAll(sensors)
    val stream = new ByteStreamAdapter(bytes)
    val out = new BufferedOutputStream(new FileOutputStream(outputPath))

    try {
      var b = stream.read()
      while (b != -1) {
        out.write(b)
        b = stream.read()
      }
    } finally {
      out.close()
      stream.close()
    }
  }

  private def encodeAll(sensors: Seq[SensorReading]): Array[Byte] = {
    val buffer = ByteBuffer.allocate(4 + sensors.size * 12)
    buffer.putInt(sensors.size)
    sensors.foreach { s =>
      buffer.putInt(s.id)
      buffer.putDouble(s.value)
    }
    buffer.array()
  }
}
