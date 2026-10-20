using Microsoft.AspNetCore.Mvc;
using CineLog.BLL.Services;

namespace CineLog.API.Controllers
{
    [ApiController]
    [Route("api/search")]
    public class SearchController : ControllerBase
    {
        private readonly ICineLogService _service;

        public SearchController(ICineLogService service)
        {
            _service = service;
        }

        [HttpGet("movies")]
        public async Task<IActionResult> Search(string title)
        {
            return Ok(await _service.SearchMoviesAsync(title));
        }
    }
}