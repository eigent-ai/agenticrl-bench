using System;
using System.Diagnostics;

namespace DataProcessor.Services
{
    public class Logger
    {
        public void WriteDebugLog(string message)
        {
#if DEBUG
            Console.WriteLine($"[DEBUG] {message}");
#endif
        }

        public void WriteInfo(string message)
        {
            Console.WriteLine($"[INFO] {message}");
        }
    }
}
