namespace PluginSystem;

public interface IProcessor<T>
{
    T Process(T input);
}
