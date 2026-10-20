namespace CineLog.BLL.DTO
{
    public class UserActivityDTO
    {
        public string ActivityType { get; set; } = string.Empty; 
        public string MovieTitle { get; set; } = string.Empty;
        public decimal? Rating { get; set; }
        public DateTime ActivityDate { get; set; }
    }
}