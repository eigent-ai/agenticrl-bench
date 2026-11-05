namespace PluginSystem;

public class ReversePlugin : IPlugin
{
    public string Name => "Reverse";

    public string Execute(string input)
    {
        var chars = input.ToCharArray();
        System.Array.Reverse(chars);
        return new string(chars);
    }
}
