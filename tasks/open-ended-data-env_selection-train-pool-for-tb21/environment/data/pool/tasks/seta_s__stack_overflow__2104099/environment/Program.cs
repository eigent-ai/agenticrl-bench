#define DEBUG
#define RELEASE
using System;
using DataProcessor.Services;

namespace DataProcessor
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== DataProcessor Application ===");

#if (DEBUG)
            Console.WriteLine("Mode=Debug");
#elif (RELEASE)
            Console.WriteLine("Mode=Release");
#endif

            var logger = new Logger();
            logger.WriteDebugLog("Application started");
            logger.WriteDebugLog("Initializing components");

            var config = new ConfigManager();
            config.PrintConfig();

            var emailNotifier = new EmailNotifier();
            emailNotifier.Run();

            logger.WriteDebugLog("Processing complete");
            Console.WriteLine("=== Done ===");
        }
    }
}
