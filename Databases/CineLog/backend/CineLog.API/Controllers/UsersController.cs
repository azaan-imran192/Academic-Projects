using Microsoft.AspNetCore.Mvc;
using CineLog.Data.Models;
using CineLog.BLL.Services;
using CineLog.BLL;

namespace CineLog.API.Controllers
{
    [ApiController]
    [Route("api/users")]
    public class UsersController : ControllerBase
    {
        private readonly CineLogContext _context;

        public UsersController(CineLogContext context)
        {
            _context = context;
        }

        private ICineLogService GetService()
        {
            return CineLogServiceFactory.Create(_context);
        }

        [HttpGet("activity/{userId:int}")]
        public async Task<IActionResult> GetUserActivity(int userId)
        {
            var service = GetService();
            var activity = await service.GetUserActivityAsync(userId);
            return Ok(activity);
        }

        [HttpGet("connections/{userId:int}")]
        public async Task<IActionResult> GetConnections(int userId)
        {
            var service = GetService();
            var connections = await service.GetFriendConnectionsAsync(userId);
            return Ok(connections);
        }

        [HttpGet("friends-activity/{userId:int}")]
        public async Task<IActionResult> GetFriendsActivity(int userId)
        {
            var service = GetService();
            var feed = await service.GetFriendsActivityFeedAsync(userId);
            return Ok(feed);
        }
    }
}