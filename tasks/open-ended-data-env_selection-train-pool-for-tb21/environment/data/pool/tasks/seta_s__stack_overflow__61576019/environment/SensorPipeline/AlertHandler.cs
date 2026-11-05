namespace SensorPipeline;

public class AlertHandler
{
    private readonly double _threshold;
    private readonly string _path;

    public AlertHandler(SensorProcessor processor, double threshold, string path)
    {
        _threshold = threshold;
        _path = path;
        processor.OnReading = HandleAlert;
    }

    private void HandleAlert(double value)
    {
        if (value > _threshold)
            File.AppendAllText(_path,
                $"{DateTime.UtcNow:o} ALERT value={value:F2} threshold={_threshold:F2}\n");
    }
}
