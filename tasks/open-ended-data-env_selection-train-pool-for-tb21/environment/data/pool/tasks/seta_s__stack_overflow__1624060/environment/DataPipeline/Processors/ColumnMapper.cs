using DataPipeline.Models;

namespace DataPipeline.Processors;

public static class ColumnMapper
{
    public static Dictionary<ColumnType, int> MapColumns(List<ColumnType> columns)
    {
        var mapping = new Dictionary<ColumnType, int>();

        foreach (var col in columns)
        {
            int index = (int)col - 1;
            mapping[col] = index;
        }

        return mapping;
    }
}
