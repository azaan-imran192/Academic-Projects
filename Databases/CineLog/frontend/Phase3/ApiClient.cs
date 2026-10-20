using CineLog.BLL.DTO;
using CineLog.Data.Models;

using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace Phase3
{
    public static class ApiClient
    {
        private static readonly string BaseUrl = (Environment.GetEnvironmentVariable("CINELOG_API_URL") ?? "http://localhost:5285/api/").TrimEnd('/') + "/";
        private static readonly HttpClient _client = new HttpClient { BaseAddress = new Uri(BaseUrl) };

        // --- 1. MOVIES ---
        public static async Task<List<VwTopRatedMovie>> GetTopRatedAsync()
        {
            return await _client.GetFromJsonAsync<List<VwTopRatedMovie>>("movies/top-rated");
        }

        public static async Task<List<Movie>> GetTrendingAsync(int days)
        {
            return await _client.GetFromJsonAsync<List<Movie>>($"movies/trending/{days}");
        }

        public static async Task<MovieDetailsDTO> GetMovieDetailsAsync(int movieId)
        {
            return await _client.GetFromJsonAsync<MovieDetailsDTO>($"movies/details/{movieId}");
        }

        public static async Task<List<Movie>> GetMoviesByGenreAsync(string genre)
        {
            return await _client.GetFromJsonAsync<List<Movie>>($"movies/genre/{genre}");
        }

        public static async Task<List<Movie>> RecommendMoviesAsync(int userId)
        {
            return await _client.GetFromJsonAsync<List<Movie>>($"movies/recommend/{userId}");
        }

        // --- REVIEWS ---
        public static async Task AddReviewAsync(int userId, int movieId, int rating, string text)
        {
            var reviewDto = new
            {
                UserId = userId,
                MovieId = movieId,
                Rating = (decimal)rating, 
                ReviewText = text
            };

            var response = await _client.PostAsJsonAsync("reviews/add", reviewDto);

            if (!response.IsSuccessStatusCode)
            {
                string errorDetails = await response.Content.ReadAsStringAsync();
                throw new Exception($"Server Error: {errorDetails}");
            }
        }


        // --- 2. SEARCH  ---
        public static async Task<List<Movie>> SearchMoviesAsync(string title)
        {
            return await _client.GetFromJsonAsync<List<Movie>>($"search/movies?title={title}");
        }

        // --- 3. USERS & SOCIAL ---
        public static async Task<List<UserActivityDTO>> GetUserActivityAsync(int userId)
        {
            return await _client.GetFromJsonAsync<List<UserActivityDTO>>($"users/activity/{userId}");
        }

        public static async Task<List<FriendConnectionDTO>> GetFriendConnectionsAsync(int userId)
        {
            return await _client.GetFromJsonAsync<List<FriendConnectionDTO>>($"users/connections/{userId}");
        }

        // --- 4. WATCHLIST ---
        public static async Task<List<Movie>> GetWatchlistAsync(int userId)
        {
            return await _client.GetFromJsonAsync<List<Movie>>($"watchlist/{userId}");
        }

        public static async Task AddToWatchlistAsync(int userId, int movieId)
        {
            await _client.PostAsync($"watchlist/add?userId={userId}&movieId={movieId}", null);
        }

        public static async Task RemoveFromWatchlistAsync(int userId, int movieId)
        {
            await _client.DeleteAsync($"watchlist/remove?userId={userId}&movieId={movieId}");
        }

        // --- 5. LISTS ---
        public static async Task<List<List>> GetUserListsAsync(int userId)
        {
            return await _client.GetFromJsonAsync<List<List>>($"lists/user/{userId}");
        }

        // --- 6. ANALYTICS (Super Users / Public Feed) ---
        public static async Task<List<SuperUserDTO>> GetSuperUsersAsync()
        {
            return await _client.GetFromJsonAsync<List<SuperUserDTO>>("analytics/super-users");
        }

        public static async Task<List<PopularGenreDTO>> GetPopularGenresAsync()
        {
            return await _client.GetFromJsonAsync<List<PopularGenreDTO>>("analytics/popular-genres");
        }

        public static async Task<List<ActivityFeedDTO>> GetPublicFeedAsync()
        {
            return await _client.GetFromJsonAsync<List<ActivityFeedDTO>>("analytics/public-feed");
        }

        // --- 5. LISTS ---



        public static async Task<List<Movie>> GetListItemsAsync(int listId)
        {
            return await _client.GetFromJsonAsync<List<Movie>>($"lists/{listId}/items");
        }

        // Create a new list
        public static async Task CreateListAsync(int userId, string title, string description)
        {
            var dto = new { UserId = userId, Title = title, Description = description };
            await _client.PostAsJsonAsync("lists/create", dto);
        }

        // Add a movie to a list
        public static async Task AddListItemAsync(int listId, int movieId)
        {
            var dto = new { ListId = listId, MovieId = movieId };
            await _client.PostAsJsonAsync("lists/add-item", dto);
        }

        // Remove a movie from a list
        public static async Task RemoveListItemAsync(int listId, int movieId)
        {
            var request = new HttpRequestMessage(HttpMethod.Delete, "lists/remove-item");
            request.Content = JsonContent.Create(new { ListId = listId, MovieId = movieId });
            await _client.SendAsync(request);
        }

        // --- 7. SYSTEM ---
        public static async Task SetModeAsync(string mode)
        {
            await _client.PostAsync($"system/mode/{mode}", null);
        }
    }
}