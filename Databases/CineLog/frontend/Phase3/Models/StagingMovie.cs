using System;
using System.Collections.Generic;

namespace CineLog.Data.Models;

public partial class StagingMovie
{
    public string? Id { get; set; }

    public string? Title { get; set; }

    public string? VoteAverage { get; set; }

    public string? VoteCount { get; set; }

    public string? Status { get; set; }

    public string? ReleaseDate { get; set; }

    public string? Revenue { get; set; }

    public string? Runtime { get; set; }

    public string? Adult { get; set; }

    public string? BackdropPath { get; set; }

    public string? Budget { get; set; }

    public string? Homepage { get; set; }

    public string? ImdbId { get; set; }

    public string? OriginalLanguage { get; set; }

    public string? OriginalTitle { get; set; }

    public string? Overview { get; set; }

    public string? Popularity { get; set; }

    public string? PosterPath { get; set; }

    public string? Tagline { get; set; }

    public string? Genres { get; set; }

    public string? ProductionCompanies { get; set; }

    public string? ProductionCountries { get; set; }

    public string? SpokenLanguages { get; set; }

    public string? Keywords { get; set; }
}