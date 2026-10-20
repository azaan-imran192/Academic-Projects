using System;

namespace CineLog.Data.Models
{
    public partial class VwTopRatedMovie
    {
        public string? Title { get; set; }
        public int? ReleaseYear { get; set; }
        public decimal? VoteAverage { get; set; }
        public int? VoteCount { get; set; }
    }
}