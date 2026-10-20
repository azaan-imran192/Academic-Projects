using System;
using System.Collections.Generic;

namespace CineLog.Data.Models;

public partial class Movie
{
    public int MovieId { get; set; }

    public string? Title { get; set; }

    public int? ReleaseYear { get; set; }

    public int? Runtime { get; set; }

    public string? Description { get; set; }

    public decimal? VoteAverage { get; set; }

    public int? VoteCount { get; set; }

    public virtual ICollection<ListItem> ListItems { get; set; } = new List<ListItem>();

    public virtual ICollection<Review> Reviews { get; set; } = new List<Review>();

    public virtual ICollection<Watchlist> Watchlists { get; set; } = new List<Watchlist>();

    public virtual ICollection<Genre> Genres { get; set; } = new List<Genre>();
}