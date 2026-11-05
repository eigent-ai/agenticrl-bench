namespace PluginSystem;

public class StringProcessor : IProcessor<string>
{
    public string Process(string input) => input.Trim().ToLower();
}
