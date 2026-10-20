using Microsoft.AspNetCore.Mvc;
using CineLog.BLL.Services;

namespace CineLog.API.Controllers
{
    [ApiController]
    [Route("api/watchlist")]
    public class WatchlistController : ControllerBase
    {
        private readonly ICineLogService _service;

        public WatchlistController(ICineLogService service)
        {
            _service = service;
        }

        [HttpPost("add")]
        public async Task<IActionResult> Add(int userId, int movieId)
        {
            await _service.AddToWatchlistAsync(userId, movieId);
            return Ok();
        }

        [HttpDelete("remove")]
        public async Task<IActionResult> Remove(int userId, int movieId)
        {
            await _service.RemoveFromWatchlistAsync(userId, movieId);
            return Ok();
        }

        [HttpGet("{userId}")]
        public async Task<IActionResult> Get(int userId)
        {
            return Ok(await _service.GetWatchlistAsync(userId));
        }
    }
}