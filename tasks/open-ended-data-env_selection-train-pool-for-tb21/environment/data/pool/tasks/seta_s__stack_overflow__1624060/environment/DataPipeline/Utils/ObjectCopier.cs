using System.Runtime.Serialization.Formatters.Binary;

namespace DataPipeline.Utils;

public static class ObjectCopier
{
    public static T Clone<T>(T source)
    {
        if (source == null)
            throw new ArgumentNullException(nameof(source));

        using var stream = new MemoryStream();
#pragma warning disable SYSLIB0011
        var formatter = new BinaryFormatter();
        formatter.Serialize(stream, source);
        stream.Position = 0;
        return (T)formatter.Deserialize(stream);
#pragma warning restore SYSLIB0011
    }
}
