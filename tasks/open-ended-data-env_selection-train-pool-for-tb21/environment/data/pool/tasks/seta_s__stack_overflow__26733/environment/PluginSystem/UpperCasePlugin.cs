namespace PluginSystem;

public class UpperCasePlugin : IPlugin
{
    public string Name => "UpperCase";

    public string Execute(string input) => input.ToUpper();
}
