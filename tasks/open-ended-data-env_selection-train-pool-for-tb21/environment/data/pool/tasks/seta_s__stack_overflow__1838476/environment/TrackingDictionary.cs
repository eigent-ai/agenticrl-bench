namespace DataIngester;

public class TrackingDictionary : Dictionary<Guid, Element>
{
    public int DuplicateCount { get; private set; }

    public new void Add(Guid key, Element value)
    {
        if (ContainsKey(key))
        {
            DuplicateCount++;
            this[key] = value;
        }
        else
        {
            base.Add(key, value);
        }
    }
}
