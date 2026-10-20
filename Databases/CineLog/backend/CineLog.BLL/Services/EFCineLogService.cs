using CineLog.BLL.DTO;
using CineLog.Data.Models;
using Microsoft.EntityFrameworkCore;

namespace CineLog.BLL.Services
{
    public class EfCineLogService : ICineLogService
    {
        private readonly CineLogContext _context;

        public EfCineLogService(CineLogContext context)
        {
            _context = context;
        }

        // 1. Top Rated Movies
        public async Task<IEnumerable<Movie>> GetTopRatedMoviesAsync()
        {
            return await _context.Movies
                .OrderByDescending(m => m.VoteAverage)
                .ThenByDescending(m => m.VoteCount)
                .Take(100)
                .AsNoTracking()
                .ToListAsync();
        }

        // 2. Movies by Genre (LINQ)
        public async Task<IEnumerable<Movie>> GetMoviesByGenreAsync(string genreName)
        {
            return await _context.Movies
                .Where(m => m.Genres.Any(g => g.GenreName == genreName))
                .OrderByDescending(m => m.VoteAverage)
                .ThenByDescending(m => m.VoteCount)
                .Take(5) // only top 5 
                .AsNoTracking()
                .ToListAsync();
        }

        // 3. Movie Details
        public async Task<MovieDetailsDTO?> GetMovieDetailsAsync(int movieId)
        {
            var movie = await _context.Movies
                .Include(m => m.Genres)
                .Include(m => m.Reviews)
                    .ThenInclude(r => r.User)
                .AsNoTracking()
                .FirstOrDefaultAsync(m => m.MovieId == movieId);

            if (movie == null)
                return null;

            return new MovieDetailsDTO
            {
                MovieID = movie.MovieId,
                Title = movie.Title ?? string.Empty,
                ReleaseYear = movie.ReleaseYear,
                VoteAverage = movie.VoteAverage ?? 0,
                VoteCount = movie.VoteCount ?? 0,
                Genres = movie.Genres
                    .Select(g => g.GenreName ?? string.Empty)
                    .ToList(),
                RecentReviews = movie.Reviews
                    .OrderByDescending(r => r.ReviewDate)
                    .Take(20)
                    .Select(r => new ReviewDTO
                    {
                        UserName = r.User?.UserName ?? string.Empty,
                        Rating = r.Rating ?? 0,
                        ReviewText = r.ReviewText ?? string.Empty,
                        ReviewDate = r.ReviewDate
                    })
                    .ToList()
            };
        }

        // 4. User Activity (LINQ)
        public async Task<IEnumerable<UserActivityDTO>> GetUserActivityAsync(int userId)
        {
            var reviews = await _context.Reviews
                .Include(r => r.Movie)
                .Where(r => r.UserId == userId)
                .Select(r => new UserActivityDTO
                {
                    ActivityType = "Review",
                    MovieTitle = r.Movie.Title ?? string.Empty,
                    Rating = r.Rating,
                    ActivityDate = r.ReviewDate
                })
                .ToListAsync();

            var watchlist = await _context.Watchlists
                .Include(w => w.Movie)
                .Where(w => w.UserId == userId)
                .Select(w => new UserActivityDTO
                {
                    ActivityType = "Watchlist",
                    MovieTitle = w.Movie.Title ?? string.Empty,
                    Rating = null,
                    ActivityDate = w.AddedDate ?? DateTime.MinValue
                })
                .ToListAsync();

            var listItems = await _context.ListItems
                .Include(li => li.List)
                .Include(li => li.Movie)
                .Where(li => li.List.UserId == userId)
                .Select(li => new UserActivityDTO
                {
                    ActivityType = "List Item",
                    MovieTitle = li.Movie.Title ?? string.Empty,
                    Rating = null,
                    ActivityDate = li.AddedDate ?? DateTime.MinValue
                })
                .ToListAsync();

            return reviews
                .Concat(watchlist)
                .Concat(listItems)
                .OrderByDescending(a => a.ActivityDate)
                .ToList();
        }

        // 5. Trending Movies (most reviewed in last N days)
        public async Task<IEnumerable<Movie>> GetTrendingMoviesAsync(int days)
        {
            var since = DateTime.Now.AddDays(-days);

            return await _context.Reviews
                .Where(r => r.ReviewDate >= since)
                .GroupBy(r => r.MovieId)
                .OrderByDescending(g => g.Count())
                .Select(g => g.First().Movie!)
                .AsNoTracking()
                .ToListAsync();
        }

        // 6. Recommended Movies by User's Top Genres
        public async Task<IEnumerable<Movie>> RecommendMoviesAsync(int userId)
        {
            var topGenres = await _context.Reviews
                .Where(r => r.UserId == userId)
                .SelectMany(r => r.Movie.Genres)
                .GroupBy(g => g.GenreId)
                .OrderByDescending(g => g.Count())
                .Take(3)
                .Select(g => g.Key)
                .ToListAsync();

            return await _context.Movies
                .Where(m => m.Genres.Any(g => topGenres.Contains(g.GenreId)))
                .OrderByDescending(m => m.VoteAverage)
                .ThenByDescending(m => m.VoteCount)
                .Take(20)
                .AsNoTracking()
                .ToListAsync();
        }

        // 7. Friend Connections 
        public async Task<IEnumerable<FriendConnectionDTO>> GetFriendConnectionsAsync(int userId)
        {
            return await _context.Follows
                .Where(f => f.FollowerId == userId)
                .Include(f => f.Followed)
                .Select(f => new FriendConnectionDTO
                {
                    UserName = f.Followed.UserName ?? string.Empty,
                    Level = 1
                })
                .AsNoTracking()
                .ToListAsync();
        }

        // REVIEWS
        public async Task<bool> AddReviewAsync(ReviewCreateDTO dto)
        {
            var entity = new Review
            {
                UserId = dto.UserId,
                MovieId = dto.MovieId,
                Rating = dto.Rating,
                ReviewText = dto.ReviewText
            };

            _context.Reviews.Add(entity);
            await _context.SaveChangesAsync();
            return true;
        }

        // WATCHLIST
        public async Task<bool> AddToWatchlistAsync(int userId, int movieId)
        {
            var exists = await _context.Watchlists
                .AnyAsync(w => w.UserId == userId && w.MovieId == movieId);

            if (exists) return false;

            _context.Watchlists.Add(new Watchlist
            {
                UserId = userId,
                MovieId = movieId,
                AddedDate = DateTime.Now
            });

            await _context.SaveChangesAsync();
            return true;
        }

        public async Task<bool> RemoveFromWatchlistAsync(int userId, int movieId)
        {
            var entry = await _context.Watchlists
                .FirstOrDefaultAsync(w => w.UserId == userId && w.MovieId == movieId);

            if (entry == null) return false;

            _context.Watchlists.Remove(entry);
            await _context.SaveChangesAsync();
            return true;
        }

        public async Task<IEnumerable<Movie>> GetWatchlistAsync(int userId)
        {
            return await _context.Watchlists
                .Where(w => w.UserId == userId)
                .Select(w => w.Movie!)
                .AsNoTracking()
                .ToListAsync();
        }

        // LISTS
        public async Task<IEnumerable<List>> GetUserListsAsync(int userId)
        {
            return await _context.Lists
                .Where(l => l.UserId == userId)
                .AsNoTracking()
                .ToListAsync();
        }

        public async Task<int> CreateListAsync(ListCreateDTO dto)
        {
            var list = new List
            {
                UserId = dto.UserId,
                Title = dto.Title,
                Description = dto.Description,
                CreatedDate = DateTime.Now
            };

            _context.Lists.Add(list);
            await _context.SaveChangesAsync();
            return list.ListId;
        }

        public async Task<bool> AddListItemAsync(int listId, int movieId)
        {
            var exists = await _context.ListItems
                .AnyAsync(li => li.ListId == listId && li.MovieId == movieId);

            if (exists) return false;

            _context.ListItems.Add(new ListItem
            {
                ListId = listId,
                MovieId = movieId,
                AddedDate = DateTime.Now
            });

            await _context.SaveChangesAsync();
            return true;
        }

        public async Task<bool> RemoveListItemAsync(int listId, int movieId)
        {
            var item = await _context.ListItems
                .FirstOrDefaultAsync(li => li.ListId == listId && li.MovieId == movieId);

            if (item == null) return false;

            _context.ListItems.Remove(item);
            await _context.SaveChangesAsync();
            return true;
        }

        public async Task<IEnumerable<Movie>> GetListItemsAsync(int listId)
        {
            return await _context.ListItems
                .Where(li => li.ListId == listId)
                .Select(li => li.Movie!)
                .AsNoTracking()
                .ToListAsync();
        }

        // SEARCH
        public async Task<IEnumerable<Movie>> SearchMoviesAsync(string query)
        {
            query = query ?? string.Empty;

            return await _context.Movies
                .Where(m => m.Title != null && m.Title.Contains(query))
                .OrderByDescending(m => m.VoteAverage)
                .AsNoTracking()
                .ToListAsync();
        }

        // Super Users
        public async Task<IEnumerable<SuperUserDTO>> GetSuperUsersAsync()
        {
            
            return await _context.VwMostActiveUsers
                .OrderByDescending(v => v.TotalReviews)
                .Select(v => new SuperUserDTO
                {
                    UserName = v.UserName ?? string.Empty,
                    TotalReviews = v.TotalReviews ?? 0
                })
                .AsNoTracking()
                .ToListAsync();
        }

        // Popular Genres
        public async Task<IEnumerable<PopularGenreDTO>> GetPopularGenresAsync()
        {
            return await _context.VwPopularGenres
                .OrderByDescending(v => v.MovieCount)
                .Select(v => new PopularGenreDTO
                {
                    GenreName = v.GenreName ?? string.Empty,
                    MovieCount = v.MovieCount ?? 0
                })
                .AsNoTracking()
                .ToListAsync();
        }

        // PUBLIC ACTIVITY FEED 
        public async Task<IEnumerable<ActivityFeedDTO>> GetPublicActivityFeedAsync()
        {
            return await _context.VwPublicActivityFeeds
                .OrderByDescending(v => v.ReviewDate)
                .Select(v => new ActivityFeedDTO
                {
                    UserName = v.UserName ?? string.Empty,
                    Title = v.Title ?? string.Empty,
                    Rating = v.Rating ?? 0,
                    ReviewText = v.ReviewText ?? string.Empty,
                    ReviewDate = v.ReviewDate
                })
                .AsNoTracking()
                .ToListAsync();
        }

        public async Task<IEnumerable<ActivityFeedDTO>> GetFriendsActivityFeedAsync(int userId)
{
     var friendIds = await _context.Follows
        .Where(f => f.FollowerId == userId && f.Followed != null)
        .Select(f => (int?)f.Followed.UserId)   
        .Distinct()
        .ToListAsync();

    if (!friendIds.Any())
    {
        return Enumerable.Empty<ActivityFeedDTO>();
    }

    var feed = await _context.Reviews
        .Include(r => r.Movie)
        .Include(r => r.User)
        .Where(r => r.UserId != null && friendIds.Contains(r.UserId)) 
        .OrderByDescending(r => r.ReviewDate)
        .Take(50)
        .Select(r => new ActivityFeedDTO
        {
            UserName   = r.User != null ? (r.User.UserName ?? string.Empty) : string.Empty,
            Title      = r.Movie != null ? (r.Movie.Title ?? string.Empty) : string.Empty,
            Rating     = r.Rating ?? 0,
            ReviewText = r.ReviewText ?? string.Empty,
            ReviewDate = r.ReviewDate
        })
        .AsNoTracking()
        .ToListAsync();

        return feed;
        }

    }
}