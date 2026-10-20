using System;
using System.Collections.Generic;

namespace CineLog.Data.Models;

public partial class Review
{
    public int ReviewId { get; set; }

    public int? UserId { get; set; }

    public int? MovieId { get; set; }

    public decimal? Rating { get; set; }

    public string? ReviewText { get; set; }

    public DateTime ReviewDate { get; set; }

    public virtual Movie? Movie { get; set; }

    public virtual User? User { get; set; }
}