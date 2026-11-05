using DataPipeline.Models;

namespace DataPipeline.Processors;

public static class DataTransformer
{
    public static List<string[]> Transform(
        List<string[]> rows,
        string[] headers,
        Dictionary<ColumnType, int> columnIndices,
        PipelineConfig config)
    {
        var result = new List<string[]>();

        foreach (var row in rows)
        {
            var transformedRow = new string[config.ColumnsToProcess.Count];

            for (int i = 0; i < config.ColumnsToProcess.Count; i++)
            {
                var colType = config.ColumnsToProcess[i];
                int sourceIndex = columnIndices[colType];

                if (sourceIndex >= row.Length)
                    throw new IndexOutOfRangeException(
                        $"Column {colType} maps to index {sourceIndex} but row only has {row.Length} columns.");

                string value = row[sourceIndex];

                string colName = colType.ToString();
                if (config.TransformRules.TryGetValue(colName, out var rule))
                {
                    value = ApplyTransform(value, rule);
                }

                transformedRow[i] = value;
            }

            result.Add(transformedRow);
        }

        return result;
    }

    private static string ApplyTransform(string value, string rule)
    {
        return rule switch
        {
            "uppercase" => value.ToUpper(),
            "format_2dp" => FormatDecimal(value),
            "trim" => value.Trim(),
            _ => value
        };
    }

    private static string FormatDecimal(string value)
    {
        if (double.TryParse(value, System.Globalization.NumberStyles.Any,
            System.Globalization.CultureInfo.InvariantCulture, out double num))
        {
            return num.ToString("F2", System.Globalization.CultureInfo.InvariantCulture);
        }
        return value;
    }
}
