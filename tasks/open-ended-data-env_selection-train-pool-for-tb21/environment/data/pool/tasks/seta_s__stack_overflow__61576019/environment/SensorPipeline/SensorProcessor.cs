namespace SensorPipeline;

public class SensorProcessor
{
    public Action<double> OnReading = delegate { };

    public void ProcessReading(double value)
    {
        OnReading(value);
    }

    public void ProcessAll(IEnumerable<double> values)
    {
        foreach (var v in values)
            ProcessReading(v);
    }
}
