namespace PluginSystem;

public interface IPlugin
{
    string Name { get; }
    string Execute(string input);
}
