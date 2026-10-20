using Microsoft.AspNetCore.Mvc;
using CineLog.BLL.DTO;
using CineLog.BLL.Services;

namespace CineLog.API.Controllers
{
    [ApiController]
    [Route("api/reviews")]
    public class ReviewsController : ControllerBase
    {
        private readonly ICineLogService _service;

        public ReviewsController(ICineLogService service)
        {
            _service = service;
        }

        [HttpPost("add")]
        public async Task<IActionResult> AddReview([FromBody] ReviewCreateDTO dto)
        {
            await _service.AddReviewAsync(dto);
            return Ok(new { message = "Review added successfully" });
        }
    }
}