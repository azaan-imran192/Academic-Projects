using System;
using System.Collections.Generic;

namespace CineLog.Data.Models;

public partial class List
{
    public int ListId { get; set; }

    public int? UserId { get; set; }

    public string? Title { get; set; }

    public string? Description { get; set; }

    public DateTime? CreatedDate { get; set; }

    public virtual ICollection<ListItem> ListItems { get; set; } = new List<ListItem>();

    public virtual User? User { get; set; }
}