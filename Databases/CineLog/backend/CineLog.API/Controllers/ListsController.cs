using Microsoft.AspNetCore.Mvc;
using CineLog.BLL.Services;
using CineLog.BLL.DTO;

namespace CineLog.API.Controllers
{
    [ApiController]
    [Route("api/lists")]
    public class ListsController : ControllerBase
    {
        private readonly ICineLogService _service;

        public ListsController(ICineLogService service)
        {
            _service = service;
        }

        [HttpGet("user/{userId}")]
        public async Task<IActionResult> GetUserLists(int userId)
        {
            return Ok(await _service.GetUserListsAsync(userId));
        }

        [HttpPost("create")]
        public async Task<IActionResult> Create(ListCreateDTO dto)
        {
            int id = await _service.CreateListAsync(dto);
            return Ok(new { listId = id });
        }

        [HttpPost("add-item")]
        public async Task<IActionResult> AddItem(ListItemDTO dto)
        {
            await _service.AddListItemAsync(dto.ListId, dto.MovieId);
            return Ok();
        }

        [HttpDelete("remove-item")]
        public async Task<IActionResult> RemoveItem(ListItemDTO dto)
        {
            await _service.RemoveListItemAsync(dto.ListId, dto.MovieId);
            return Ok();
        }

        [HttpGet("{listId}/items")]
        public async Task<IActionResult> GetItems(int listId)
        {
            return Ok(await _service.GetListItemsAsync(listId));
        }
    }
}
