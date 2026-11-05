namespace DataPipeline.Models;

[Serializable]
public class PipelineConfig
{
    public List<ColumnType> ColumnsToProcess { get; set; }
    public string OutputDelimiter { get; set; }
    public bool IncludeHeader { get; set; }
    public Dictionary<string, string> TransformRules { get; set; }

    public PipelineConfig()
    {
        ColumnsToProcess = new List<ColumnType>();
        OutputDelimiter = ",";
        IncludeHeader = true;
        TransformRules = new Dictionary<string, string>
        {
            { "default_action", "none" }
        };
    }
}
