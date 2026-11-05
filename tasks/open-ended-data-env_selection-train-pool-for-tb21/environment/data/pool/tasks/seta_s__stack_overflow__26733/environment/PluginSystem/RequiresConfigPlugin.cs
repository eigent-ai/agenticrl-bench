namespace PluginSystem;

public class RequiresConfigPlugin : IPlugin
{
    private readonly string _prefix;

    public RequiresConfigPlugin(string prefix)
    {
        _prefix = prefix;
    }

    public string Name => "RequiresConfig";

    public string Execute(string input) => $"{_prefix}: {input}";
}
