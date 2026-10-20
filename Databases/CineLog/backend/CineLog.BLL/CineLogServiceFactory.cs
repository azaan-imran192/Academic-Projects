using CineLog.BLL.Services;
using CineLog.Data.Models;

namespace CineLog.BLL
{
    public static class CineLogServiceFactory
    {
        private static string _mode = "ef";

        public static void SetMode(string mode)
        {
            _mode = mode?.ToLowerInvariant() == "sp" ? "sp" : "ef";
        }

        public static string GetMode() => _mode;

        public static ICineLogService Create(CineLogContext context)
        {
            return _mode switch
            {
                "sp" => new SpCineLogService(context),
                _ => new EfCineLogService(context),
            };
        }
    }
}