USE CineLog
GO

CREATE INDEX IX_Movies_VoteAverage ON Movies(VoteAverage);
CREATE INDEX IX_Movies_VoteCount   ON Movies(VoteCount);
CREATE INDEX IX_MovieGenres_GenreID ON MovieGenres(GenreID);
CREATE INDEX IX_MovieGenres_MovieID ON MovieGenres(MovieID);
CREATE INDEX IX_Reviews_MovieID_Date ON Reviews(MovieID, ReviewDate);
-- CREATE INDEX IX_Reviews_UserID ON Reviews(UserID);
CREATE INDEX IX_Watchlist_UserID ON Watchlist(UserID);
CREATE INDEX IX_ListItem_ListID ON ListItem(ListID);
GO


CREATE OR ALTER PROCEDURE proced_GetMovieById
    @MovieID INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        MovieID,
        Title,
        ReleaseYear,
        Runtime,
        Description,
        VoteAverage,
        VoteCount
    FROM Movies
    WHERE MovieID = @MovieID;
END;
GO


CREATE OR ALTER PROCEDURE proced_GetMovieGenres
    @MovieID INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT g.GenreName
    FROM MovieGenres mg
    JOIN Genres g ON mg.GenreID = g.GenreID
    WHERE mg.MovieID = @MovieID;
END;
GO

CREATE OR ALTER PROCEDURE proced_GetMovieReviews
    @MovieID INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT TOP 20 
        u.UserName,
        r.Rating,
        r.ReviewText,
        r.ReviewDate
    FROM Reviews r
    JOIN Users u ON r.UserID = u.UserID
    WHERE r.MovieID = @MovieID
    ORDER BY r.ReviewDate DESC;
END;
GO


-- ========================================
-- Top Rated Movies (replaces raw SELECT TOP 100)
-- ========================================
IF OBJECT_ID('proced_GetTopRatedMovies', 'P') IS NOT NULL
    DROP PROCEDURE proced_GetTopRatedMovies;
GO

CREATE PROCEDURE proced_GetTopRatedMovies
AS
BEGIN
    SET NOCOUNT ON;

    SELECT TOP 100
        m.MovieID,
        m.Title,
        m.ReleaseYear,
        m.Runtime,
        m.Description,
        m.VoteAverage,
        m.VoteCount
    FROM Movies m
    WHERE m.VoteCount > 50
    ORDER BY m.VoteAverage DESC, m.VoteCount DESC;
END;
GO



-- ========================================
-- WATCHLIST: Add
-- ========================================
IF OBJECT_ID('proced_AddToWatchlist', 'P') IS NOT NULL
    DROP PROCEDURE proced_AddToWatchlist;
GO

CREATE PROCEDURE proced_AddToWatchlist
    @UserID  INT,
    @MovieID INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Optional: validate user & movie exist
    IF NOT EXISTS (SELECT 1 FROM Users WHERE UserID = @UserID)
        THROW 50001, 'User does not exist.', 1;

    IF NOT EXISTS (SELECT 1 FROM Movies WHERE MovieID = @MovieID)
        THROW 50002, 'Movie does not exist.', 1;

    -- Avoid duplicates
    IF NOT EXISTS (
        SELECT 1
        FROM Watchlist
        WHERE UserID = @UserID AND MovieID = @MovieID
    )
    BEGIN
        INSERT INTO Watchlist (UserID, MovieID, AddedDate)
        VALUES (@UserID, @MovieID, GETDATE());
    END
END;
GO

-- ========================================
-- WATCHLIST: Remove
-- ========================================
IF OBJECT_ID('proced_RemoveFromWatchlist', 'P') IS NOT NULL
    DROP PROCEDURE proced_RemoveFromWatchlist;
GO

CREATE PROCEDURE proced_RemoveFromWatchlist
    @UserID  INT,
    @MovieID INT
AS
BEGIN
    SET NOCOUNT ON;

    DELETE FROM Watchlist
    WHERE UserID = @UserID
      AND MovieID = @MovieID;
END;
GO

-- ========================================
-- WATCHLIST: Get movies in a user's watchlist
-- ========================================
IF OBJECT_ID('proced_GetWatchlist', 'P') IS NOT NULL
    DROP PROCEDURE proced_GetWatchlist;
GO

CREATE PROCEDURE proced_GetWatchlist
    @UserID INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT m.*
    FROM Movies m
    JOIN Watchlist w ON m.MovieID = w.MovieID
    WHERE w.UserID = @UserID;
END;
GO



-- ========================================
-- LISTS: Get lists for a user
-- ========================================
IF OBJECT_ID('proced_GetUserLists', 'P') IS NOT NULL
    DROP PROCEDURE proced_GetUserLists;
GO

CREATE PROCEDURE proced_GetUserLists
    @UserID INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT *
    FROM Lists
    WHERE UserID = @UserID
    ORDER BY CreatedDate DESC;
END;
GO

-- ========================================
-- LISTS: Create list and return ListID
-- ========================================
IF OBJECT_ID('proced_CreateList', 'P') IS NOT NULL
    DROP PROCEDURE proced_CreateList;
GO

CREATE PROCEDURE proced_CreateList
    @UserID      INT,
    @Title       NVARCHAR(100),
    @Description NVARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;

    IF NOT EXISTS (SELECT 1 FROM Users WHERE UserID = @UserID)
        THROW 50003, 'User does not exist.', 1;

    INSERT INTO Lists (UserID, Title, Description, CreatedDate)
    VALUES (@UserID, @Title, @Description, GETDATE());

    SELECT CAST(SCOPE_IDENTITY() AS INT) AS ListID;
END;
GO

-- ========================================
-- LIST ITEMS: Add movie to list
-- ========================================
IF OBJECT_ID('proced_AddListItem', 'P') IS NOT NULL
    DROP PROCEDURE proced_AddListItem;
GO

CREATE PROCEDURE proced_AddListItem
    @ListID  INT,
    @MovieID INT
AS
BEGIN
    SET NOCOUNT ON;

    IF NOT EXISTS (SELECT 1 FROM Lists WHERE ListID = @ListID)
        THROW 50004, 'List does not exist.', 1;

    IF NOT EXISTS (SELECT 1 FROM Movies WHERE MovieID = @MovieID)
        THROW 50005, 'Movie does not exist.', 1;

    IF NOT EXISTS (
        SELECT 1
        FROM ListItem
        WHERE ListID = @ListID AND MovieID = @MovieID
    )
    BEGIN
        INSERT INTO ListItem (ListID, MovieID, AddedDate)
        VALUES (@ListID, @MovieID, GETDATE());
    END
END;
GO

-- ========================================
-- LIST ITEMS: Remove movie from list
-- ========================================
IF OBJECT_ID('proced_RemoveListItem', 'P') IS NOT NULL
    DROP PROCEDURE proced_RemoveListItem;
GO

CREATE PROCEDURE proced_RemoveListItem
    @ListID  INT,
    @MovieID INT
AS
BEGIN
    SET NOCOUNT ON;

    DELETE FROM ListItem
    WHERE ListID = @ListID
      AND MovieID = @MovieID;
END;
GO

-- ========================================
-- LIST ITEMS: Get movies in a list
-- ========================================
IF OBJECT_ID('proced_GetListItems', 'P') IS NOT NULL
    DROP PROCEDURE proced_GetListItems;
GO

CREATE PROCEDURE proced_GetListItems
    @ListID INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT m.*
    FROM Movies m
    JOIN ListItem li ON m.MovieID = li.MovieID
    WHERE li.ListID = @ListID;
END;
GO


-- ========================================
-- Search Movies by Title
-- ========================================
IF OBJECT_ID('proced_SearchMovies', 'P') IS NOT NULL
    DROP PROCEDURE proced_SearchMovies;
GO

CREATE PROCEDURE proced_SearchMovies
    @Query NVARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    SET @Query = ISNULL(@Query, '');

    SELECT *
    FROM Movies
    WHERE Title IS NOT NULL
      AND Title LIKE '%' + @Query + '%'
    ORDER BY VoteAverage DESC, VoteCount DESC;
END;
GO


-- ========================================
-- Popular Genres (wraps vw_PopularGenres)
-- ========================================
IF OBJECT_ID('proced_GetPopularGenres', 'P') IS NOT NULL
    DROP PROCEDURE proced_GetPopularGenres;
GO

CREATE PROCEDURE proced_GetPopularGenres
AS
BEGIN
    SET NOCOUNT ON;

    SELECT GenreName, MovieCount
    FROM vw_PopularGenres;
END;
GO

-- ========================================
-- Public Activity Feed (wraps vw_PublicActivityFeed)
-- ========================================
IF OBJECT_ID('proced_GetPublicActivityFeed', 'P') IS NOT NULL
    DROP PROCEDURE proced_GetPublicActivityFeed;
GO

CREATE PROCEDURE proced_GetPublicActivityFeed
AS
BEGIN
    SET NOCOUNT ON;

    SELECT UserName, Title, Rating, ReviewText, ReviewDate
    FROM vw_PublicActivityFeed;
END;
GO





CREATE OR ALTER PROCEDURE proced_AddReview
    @UserId     INT,
    @MovieId    INT,
    @Rating     DECIMAL(3,1),
    @ReviewText NVARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Reviews (UserID, MovieID, Rating, ReviewText, ReviewDate)
    VALUES (@UserId, @MovieId, @Rating, @ReviewText, GETDATE());
END;
GO


CREATE OR ALTER TRIGGER trg_ValidateReviewDate
ON Reviews
AFTER INSERT
AS
BEGIN
    RETURN;
END;
GO





SELECT 
    s.name  AS SchemaName,
    p.name  AS ProcedureName
FROM sys.procedures p
JOIN sys.schemas s ON p.schema_id = s.schema_id
ORDER BY s.name, p.name;













USE CineLog;
GO

CREATE OR ALTER PROCEDURE dbo.sp_GetMoviesByGenre
    @GenreName NVARCHAR(100),
    @Top INT = 200
AS
BEGIN
    SET NOCOUNT ON;

    SELECT TOP (@Top)
        m.MovieID,
        m.Title,
        m.ReleaseYear,
        m.VoteAverage,
        m.VoteCount
    FROM Genres g
    JOIN MovieGenres mg ON mg.GenreID = g.GenreID
    JOIN Movies m ON m.MovieID = mg.MovieID
    WHERE g.GenreName = @GenreName
    ORDER BY m.VoteAverage DESC, m.VoteCount DESC;
END;
GO


CREATE OR ALTER PROCEDURE dbo.proced_GetTrendingMovies
    @Days INT,
    @Top INT = 50
AS
BEGIN
    SET NOCOUNT ON;

    SELECT TOP (@Top)
        m.MovieID,
        m.Title,
        COUNT(r.ReviewID) AS RecentReviews
    FROM Reviews r
    JOIN Movies m ON m.MovieID = r.MovieID
    WHERE r.ReviewDate >= DATEADD(DAY, -@Days, GETDATE())
    GROUP BY m.MovieID, m.Title
    ORDER BY COUNT(r.ReviewID) DESC;
END;
GO


USE CineLog;
GO
SELECT name FROM sys.procedures WHERE name LIKE '%Recommend%';


-- Original exploratory calls retained for reference, not run during setup.
-- EXEC dbo.proced_RecommendMovies 1; -- Run manually after its definition below.
-- EXEC dbo.sp_RecommendMovies 1; -- No definition was supplied for this name.


GO
CREATE OR ALTER PROCEDURE dbo.proced_RecommendMovies
    @UserID INT,
    @Top INT = 50
AS
BEGIN
    SET NOCOUNT ON;

    ;WITH UserGenres AS (
        SELECT TOP 5 mg.GenreID, COUNT(*) AS cnt
        FROM Reviews r
        JOIN MovieGenres mg ON mg.MovieID = r.MovieID
        WHERE r.UserID = @UserID
        GROUP BY mg.GenreID
        ORDER BY COUNT(*) DESC
    ),
    Excluded AS (
        SELECT MovieID FROM Reviews   WHERE UserID = @UserID
        UNION
        SELECT MovieID FROM Watchlist WHERE UserID = @UserID
    )
    SELECT TOP (@Top)
        m.MovieID     AS MovieID,
        m.Title       AS Title,
        m.ReleaseYear AS ReleaseYear,
        m.VoteAverage AS VoteAverage,
        m.VoteCount   AS VoteCount
    FROM Movies m
    JOIN MovieGenres mg ON mg.MovieID = m.MovieID
    JOIN UserGenres ug ON ug.GenreID = mg.GenreID
    LEFT JOIN Excluded e ON e.MovieID = m.MovieID
    WHERE e.MovieID IS NULL
    ORDER BY ug.cnt DESC, m.VoteAverage DESC, m.VoteCount DESC;
END;
GO



