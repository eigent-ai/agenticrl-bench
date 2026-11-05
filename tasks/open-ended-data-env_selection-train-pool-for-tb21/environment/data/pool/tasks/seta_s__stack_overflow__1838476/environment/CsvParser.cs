namespace DataIngester;

public static class CsvParser
{
    public static IEnumerable<Element> Parse(string filePath)
    {
        using var reader = new StreamReader(filePath);
        string? header = reader.ReadLine();
        if (header == null) yield break;

        string? line;
        while ((line = reader.ReadLine()) != null)
        {
            var parts = line.Split(',', 2);
            if (parts.Length < 2) continue;

            if (Guid.TryParse(parts[0].Trim(), out var id))
            {
                yield return new Element
                {
                    ID = id,
                    Name = parts[1].Trim()
                };
            }
        }
    }
}
