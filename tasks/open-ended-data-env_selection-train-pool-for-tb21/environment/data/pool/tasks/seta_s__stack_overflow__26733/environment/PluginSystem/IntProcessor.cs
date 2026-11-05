namespace PluginSystem;

public class IntProcessor : IProcessor<int>
{
    public int Process(int input) => input * 2;
}
