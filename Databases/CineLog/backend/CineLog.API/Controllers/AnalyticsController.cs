using Microsoft.AspNetCore.Mvc;
using CineLog.BLL.Services;

namespace CineLog.API.Controllers
{
    [ApiController]
    [Route("api/analytics")]
    public class AnalyticsController : ControllerBase
    {
        private readonly ICineLogService _service;

        public AnalyticsController(ICineLogService service)
        {
            _service = service;
        }

        [HttpGet("super-users")]
        public async Task<IActionResult> GetSuperUsers()
        {
            return Ok(await _service.GetSuperUsersAsync());
        }

        [HttpGet("popular-genres")]
        public async Task<IActionResult> GetPopularGenres()
        {
            return Ok(await _service.GetPopularGenresAsync());
        }

        [HttpGet("public-feed")]
        public async Task<IActionResult> GetPublicFeed()
        {
            return Ok(await _service.GetPublicActivityFeedAsync());
        }
    }
}