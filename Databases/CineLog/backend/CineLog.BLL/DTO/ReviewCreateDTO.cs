namespace CineLog.BLL.DTO
{
    public class ReviewCreateDTO
    {
        public int UserId { get; set; }
        public int MovieId { get; set; }
        public decimal Rating { get; set; }
        public string ReviewText { get; set; } = string.Empty;
    }
}