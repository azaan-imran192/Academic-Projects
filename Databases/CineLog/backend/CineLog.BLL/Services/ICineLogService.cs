using CineLog.BLL.DTO;
using CineLog.Data.Models;

namespace CineLog.BLL.Services
{
    public interface ICineLogService
    {
        
        Task<IEnumerable<Movie>> GetTopRatedMoviesAsync();
        Task<IEnumerable<Movie>> GetMoviesByGenreAsync(string genreName);
        Task<MovieDetailsDTO?> GetMovieDetailsAsync(int movieId);
        Task<IEnumerable<UserActivityDTO>> GetUserActivityAsync(int userId);
        Task<IEnumerable<Movie>> GetTrendingMoviesAsync(int days);
        Task<IEnumerable<Movie>> RecommendMoviesAsync(int userId);
        Task<IEnumerable<FriendConnectionDTO>> GetFriendConnectionsAsync(int userId);

        Task<bool> AddReviewAsync(ReviewCreateDTO dto);

        Task<bool> AddToWatchlistAsync(int userId, int movieId);
        Task<bool> RemoveFromWatchlistAsync(int userId, int movieId);
        Task<IEnumerable<Movie>> GetWatchlistAsync(int userId);

        Task<IEnumerable<List>> GetUserListsAsync(int userId);
        Task<int> CreateListAsync(ListCreateDTO dto);
        Task<bool> AddListItemAsync(int listId, int movieId);
        Task<bool> RemoveListItemAsync(int listId, int movieId);
        Task<IEnumerable<Movie>> GetListItemsAsync(int listId);

        Task<IEnumerable<Movie>> SearchMoviesAsync(string query);

        Task<IEnumerable<SuperUserDTO>> GetSuperUsersAsync();
        Task<IEnumerable<PopularGenreDTO>> GetPopularGenresAsync();
        Task<IEnumerable<ActivityFeedDTO>> GetPublicActivityFeedAsync();

        Task<IEnumerable<ActivityFeedDTO>> GetFriendsActivityFeedAsync(int userId);
    }
}