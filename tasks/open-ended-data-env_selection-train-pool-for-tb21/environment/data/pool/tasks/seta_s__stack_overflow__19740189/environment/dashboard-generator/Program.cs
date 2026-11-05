using System;

namespace DashboardApp
{
    class Program
    {
        static int Main(string[] args)
        {
            try
            {
                string outputDir = Path.Combine(Directory.GetCurrentDirectory(), "output");
                if (!Directory.Exists(outputDir))
                {
                    Directory.CreateDirectory(outputDir);
                }

                string outputPath = Path.Combine(outputDir, "dashboard.png");
                var generator = new DashboardGenerator();
                generator.Generate(outputPath);

                Console.WriteLine($"Dashboard generated successfully at {outputPath}");
                return 0;
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"Error generating dashboard: {ex}");
                return 1;
            }
        }
    }
}
