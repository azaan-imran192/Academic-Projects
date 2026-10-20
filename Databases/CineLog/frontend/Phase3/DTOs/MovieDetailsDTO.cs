namespace CineLog.BLL.DTO
{
    public class MovieDetailsDTO
    {
        public int MovieID { get; set; }
        public string Title { get; set; } = string.Empty;
        public int? ReleaseYear { get; set; }
        public decimal VoteAverage { get; set; }
        public int? VoteCount { get; set; }

        public List<string> Genres { get; set; } = new();
        public List<ReviewDTO> RecentReviews { get; set; } = new();
    }
}