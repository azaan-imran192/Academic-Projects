using System;
using System.Collections.Generic;

namespace CineLog.Data.Models;

public partial class ListItem
{
    public int ListItemId { get; set; }

    public int ListId { get; set; }

    public int MovieId { get; set; }

    public DateTime? AddedDate { get; set; }

    public virtual List List { get; set; } = null!;

    public virtual Movie Movie { get; set; } = null!;
}