using System;
using System.Collections.Generic;

namespace CineLog.Data.Models;

public partial class VwPublicActivityFeed
{
    public string? UserName { get; set; }

    public string? Title { get; set; }

    public decimal? Rating { get; set; }

    public string? ReviewText { get; set; }

    public DateTime ReviewDate { get; set; }
}