using CineLog.BLL;
using Microsoft.AspNetCore.Mvc;

namespace CineLog.API.Controllers
{
    [Route("api/system")]
    [ApiController]
    public class SystemController : ControllerBase
    {
        [HttpGet("mode")]
        public IActionResult GetMode()
        {
            return Ok(new { mode = CineLogServiceFactory.GetMode() });
        }

        [HttpPost("mode/{mode}")]
        public IActionResult SetMode(string mode)
        {
            CineLogServiceFactory.SetMode(mode);
            return Ok(new { message = "Mode changed.", activeMode = CineLogServiceFactory.GetMode() });
        }
    }
}