namespace CineLog.BLL.DTO
{
    public class ActivityFeedDTO
    {
        public string UserName { get; set; } = string.Empty;
        public string Title { get; set; } = string.Empty;
        public decimal Rating { get; set; }
        public string ReviewText { get; set; } = string.Empty;
        public DateTime ReviewDate { get; set; }
    }
}