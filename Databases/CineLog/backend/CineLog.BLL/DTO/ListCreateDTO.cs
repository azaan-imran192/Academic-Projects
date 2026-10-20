namespace CineLog.BLL.DTO
{
    public class ListCreateDTO
    {
        public int UserId { get; set; }
        public string Title { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
    }
}