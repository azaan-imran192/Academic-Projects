using CineLog.BLL.DTO;
using CineLog.Data.Models;
using Microsoft.EntityFrameworkCore;

namespace CineLog.BLL.Services
{
    public class SpCineLogService : ICineLogService
    {
        private readonly CineLogContext _context;

        public SpCineLogService(CineLogContext context)
        {
            _context = context;
        }

        // 1. TOP RATED MOVIES (Stored Procedure: proced_GetTopRatedMovies)
        public async Task<IEnumerable<Movie>> GetTopRatedMoviesAsync()
        {
            var rows = await _context.Movies
                .FromSqlRaw("EXEC proced_GetTopRatedMovies")
                .AsNoTracking()
                .ToListAsync();

            return rows;
        }

        // 2. MOVIES BY GENRE (SP: Proced_GetMoviesByGenre)
        public async Task<IEnumerable<Movie>> GetMoviesByGenreAsync(string genreName)
        {
            var rows = await _context.Database
                .SqlQueryRaw<MovieByGenreRow>(
                    "EXEC dbo.sp_GetMoviesByGenre @p0, @p1",
                    genreName, 200)   
                .ToListAsync();

            return rows.Select(r => new Movie
            {
                MovieId     = r.MovieID,
                Title       = r.Title,
                ReleaseYear = r.ReleaseYear,
                VoteAverage = r.VoteAverage,
                VoteCount   = r.VoteCount
            }).ToList();
        }


        // 3. MOVIE DETAILS (SPs: proced_GetMovieById, proced_GetMovieGenres, proced_GetMovieReviews)
        public async Task<MovieDetailsDTO?> GetMovieDetailsAsync(int movieId)
        {
            var movieRows = await _context.Movies
                .FromSqlInterpolated($"EXEC proced_GetMovieById {movieId}")
                .AsNoTracking()
                .ToListAsync();

            var movie = movieRows.FirstOrDefault();

            if (movie == null)
                return null;

            var genres = await _context.Database
                .SqlQueryRaw<string>("EXEC proced_GetMovieGenres @p0", movieId)
                .ToListAsync();

            var reviews = await _context.Database
                .SqlQueryRaw<ReviewDTO>("EXEC proced_GetMovieReviews @p0", movieId)
                .ToListAsync();

            return new MovieDetailsDTO
            {
                MovieID       = movie.MovieId,
                Title         = movie.Title ?? string.Empty,
                ReleaseYear   = movie.ReleaseYear,
                VoteAverage   = movie.VoteAverage ?? 0,
                VoteCount     = movie.VoteCount ?? 0,
                Genres        = genres.Select(g => g ?? string.Empty).ToList(),
                RecentReviews = reviews
            };
        }


        // 4. USER ACTIVITY (SP: proced_GetUserActivity)
        public async Task<IEnumerable<UserActivityDTO>> GetUserActivityAsync(int userId)
        {
            var rows = await _context.Database
                .SqlQueryRaw<UserActivityRow>(
                    "EXEC proced_GetUserActivity @p0",
                    userId)
                .ToListAsync();

            return rows
                .Select(r => new UserActivityDTO
                {
                    ActivityType = r.ActivityType ?? string.Empty,
                    MovieTitle   = r.Title ?? string.Empty,
                    Rating       = r.Rating,
                    ActivityDate = r.ActivityDate
                })
                .OrderByDescending(a => a.ActivityDate)
                .ToList();
        }

        // 5. TRENDING MOVIES (SP: proced_GetTrendingMovies)
        public async Task<IEnumerable<Movie>> GetTrendingMoviesAsync(int days)
        {
            var rows = await _context.Database
                .SqlQueryRaw<TrendingMovieRow>(
                    "EXEC dbo.proced_GetTrendingMovies @p0, @p1",
                    days, 50)
                .ToListAsync();


            return rows.Select(r => new Movie
            {
                MovieId = r.MovieID,
                Title   = r.Title
            }).ToList();
        }

        // 6. RECOMMENDED MOVIES (SP: proced_RecommendMovies)
        public async Task<IEnumerable<Movie>> RecommendMoviesAsync(int userId)
        {
            var rows = await _context.Database
                .SqlQueryRaw<MovieByGenreRow>(
                    "EXEC dbo.proced_RecommendMovies @p0, @p1",
                    userId, 50)  
                .ToListAsync();

            return rows.Select(r => new Movie
            {
                MovieId     = r.MovieID,
                Title       = r.Title,
                ReleaseYear = r.ReleaseYear,
                VoteAverage = r.VoteAverage,
                VoteCount   = r.VoteCount
            }).ToList();
        }


        // 7. FRIEND CONNECTIONS (SP: proced_FindFriendConnections)
        public async Task<IEnumerable<FriendConnectionDTO>> GetFriendConnectionsAsync(int userId)
        {
            var rows = await _context.Database
                .SqlQueryRaw<FriendConnectionDTO>(
                    "EXEC proced_FindFriendConnections @p0",
                    userId)
                .ToListAsync();

            return rows;
        }

        // REVIEWS (SP: proced_AddReview)
        public async Task<bool> AddReviewAsync(ReviewCreateDTO dto)
        {
            await _context.Database.ExecuteSqlInterpolatedAsync(
                $"EXEC proced_AddReview {dto.UserId}, {dto.MovieId}, {dto.Rating}, {dto.ReviewText}");

            return true;
        }

        // WATCHLIST (SPs: proced_AddToWatchlist, proced_RemoveFromWatchlist, proced_GetWatchlist)
        public async Task<bool> AddToWatchlistAsync(int userId, int movieId)
        {
            await _context.Database.ExecuteSqlInterpolatedAsync(
                $"EXEC proced_AddToWatchlist {userId}, {movieId}");

            return true;
        }

        public async Task<bool> RemoveFromWatchlistAsync(int userId, int movieId)
        {
            await _context.Database.ExecuteSqlInterpolatedAsync(
                $"EXEC proced_RemoveFromWatchlist {userId}, {movieId}");

            return true;
        }

        public async Task<IEnumerable<Movie>> GetWatchlistAsync(int userId)
        {
            var rows = await _context.Movies
                .FromSqlInterpolated($"EXEC proced_GetWatchlist {userId}")
                .AsNoTracking()
                .ToListAsync();

            return rows;
        }

        // LISTS (SPs: proced_GetUserLists, proced_CreateList, proced_AddListItem, proced_RemoveListItem, proced_GetListItems)
        public async Task<IEnumerable<List>> GetUserListsAsync(int userId)
        {
            var rows = await _context.Lists
                .FromSqlInterpolated($"EXEC proced_GetUserLists {userId}")
                .AsNoTracking()
                .ToListAsync();

            return rows;
        }

        public async Task<int> CreateListAsync(ListCreateDTO dto)
        {
            var ids = await _context.Database
                .SqlQueryRaw<int>(
                    "EXEC proced_CreateList @p0, @p1, @p2",
                    dto.UserId, dto.Title, dto.Description)
                .ToListAsync();

            return ids.FirstOrDefault();
        }

        public async Task<bool> AddListItemAsync(int listId, int movieId)
        {
            await _context.Database.ExecuteSqlInterpolatedAsync(
                $"EXEC proced_AddListItem {listId}, {movieId}");

            return true;
        }

        public async Task<bool> RemoveListItemAsync(int listId, int movieId)
        {
            await _context.Database.ExecuteSqlInterpolatedAsync(
                $"EXEC proced_RemoveListItem {listId}, {movieId}");

            return true;
        }

        public async Task<IEnumerable<Movie>> GetListItemsAsync(int listId)
        {
            var rows = await _context.Movies
                .FromSqlInterpolated($"EXEC proced_GetListItems {listId}")
                .AsNoTracking()
                .ToListAsync();

            return rows;
        }

        // SEARCH (SP: proced_SearchMovies)
        public async Task<IEnumerable<Movie>> SearchMoviesAsync(string query)
        {
            query ??= string.Empty;

            var rows = await _context.Movies
                .FromSqlInterpolated($"EXEC proced_SearchMovies {query}")
                .AsNoTracking()
                .ToListAsync();

            return rows;
        }

        // ANALYTICS (SPs: proced_GetSuperUsers, proced_GetPopularGenres, proced_GetPublicActivityFeed)
        public async Task<IEnumerable<SuperUserDTO>> GetSuperUsersAsync()
        {
            var rows = await _context.Database
                .SqlQueryRaw<SuperUserDTO>("EXEC proced_GetSuperUsers")
                .ToListAsync();

            return rows;
        }

        public async Task<IEnumerable<PopularGenreDTO>> GetPopularGenresAsync()
        {
            var rows = await _context.Database
                .SqlQueryRaw<PopularGenreDTO>("EXEC proced_GetPopularGenres")
                .ToListAsync();

            return rows;
        }

        public async Task<IEnumerable<ActivityFeedDTO>> GetPublicActivityFeedAsync()
        {
            var rows = await _context.Database
                .SqlQueryRaw<ActivityFeedDTO>("EXEC proced_GetPublicActivityFeed")
                .ToListAsync();

            return rows;
        }

        // FRIENDS ACTIVITY FEED (SP: proced_GetFriendsActivityFeed)
        public async Task<IEnumerable<ActivityFeedDTO>> GetFriendsActivityFeedAsync(int userId)
        {
            var rows = await _context.Database
                .SqlQueryRaw<ActivityFeedDTO>(
                    "EXEC proced_GetFriendsActivityFeed @p0",
                    userId)
                .ToListAsync();

            return rows;
        }

        private sealed class MovieByGenreRow
        {
            public int MovieID { get; set; }
            public string? Title { get; set; }
            public int? ReleaseYear { get; set; }
            public decimal? VoteAverage { get; set; }
            public int? VoteCount { get; set; }
        }

        private sealed class TrendingMovieRow
        {
            public int MovieID { get; set; }
            public string? Title { get; set; }
            public int RecentReviews { get; set; }
        }

        private sealed class UserActivityRow
        {
            public string? ActivityType { get; set; }
            public string? Title { get; set; }
            public decimal? Rating { get; set; }
            public DateTime ActivityDate { get; set; }
        }
    }
}