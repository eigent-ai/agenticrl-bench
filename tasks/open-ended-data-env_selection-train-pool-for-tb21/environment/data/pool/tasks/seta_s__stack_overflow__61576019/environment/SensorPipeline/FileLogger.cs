namespace SensorPipeline;

public class FileLogger
{
    private readonly string _path;

    public FileLogger(SensorProcessor processor, string path)
    {
        _path = path;
        processor.OnReading += Log;
    }

    private void Log(double value)
    {
        File.AppendAllText(_path, $"{DateTime.UtcNow:o} READING {value:F2}\n");
    }
}
