using Microsoft.AspNetCore.Mvc;
using CineLog.BLL.Services;

namespace CineLog.API.Controllers
{
    [ApiController]
    [Route("api/movies")]
    public class MoviesController : ControllerBase
    {
        private readonly ICineLogService _service;

        public MoviesController(ICineLogService service)
        {
            _service = service;
        }

        [HttpGet("top-rated")]
        public async Task<IActionResult> GetTopRated()
        {
            return Ok(await _service.GetTopRatedMoviesAsync());
        }

        [HttpGet("genre/{genreName}")]
        public async Task<IActionResult> GetByGenre(string genreName)
        {
            return Ok(await _service.GetMoviesByGenreAsync(genreName));
        }

        [HttpGet("details/{movieId}")]
        public async Task<IActionResult> GetDetails(int movieId)
        {
            var movie = await _service.GetMovieDetailsAsync(movieId);

            if (movie == null)
                return NotFound(new { message = "Movie not found" });

            return Ok(movie);
        }

        [HttpGet("trending/{days}")]
        public async Task<IActionResult> GetTrending(int days)
        {
            return Ok(await _service.GetTrendingMoviesAsync(days));
        }

        [HttpGet("recommend/{userId}")]
        public async Task<IActionResult> Recommend(int userId)
        {
            return Ok(await _service.RecommendMoviesAsync(userId));
        }
    }
}
