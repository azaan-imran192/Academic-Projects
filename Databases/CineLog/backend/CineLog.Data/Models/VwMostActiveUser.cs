using System;
using System.Collections.Generic;

namespace CineLog.Data.Models;

public partial class VwMostActiveUser
{
    public int UserId { get; set; }

    public string? UserName { get; set; }

    public int? TotalReviews { get; set; }
}