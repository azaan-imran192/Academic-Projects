:ON ERROR EXIT
-- SQLCMD mode required. Fresh local database only. No automatic database deletion.
-- PROJECT PHASE 2
-- GROUP 10: CineLog Database Implementation

-- 1. DATABASE SETUP & CLEANUP
USE master;
GO

IF DB_ID(N'CineLog') IS NOT NULL
    THROW 50001, 'CineLog already exists. Use a fresh isolated SQL Server instance; existing databases are never reset.', 1;
GO

CREATE DATABASE CineLog;
GO
USE CineLog;
GO

-- 2. PARTITIONING SETUP
CREATE PARTITION FUNCTION partition_ReviewDate (DATETIME)
AS RANGE RIGHT FOR VALUES ('2020-01-01', '2021-01-01', '2022-01-01', '2023-01-01', '2024-01-01');
GO

CREATE PARTITION SCHEME partition_ReviewDate
AS PARTITION partition_ReviewDate
ALL TO ([PRIMARY]);
GO

-- 3. CREATE TABLES

CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY(1,1),
    UserName NVARCHAR(100),
    Email NVARCHAR(100),
    JoinDate DATETIME DEFAULT GETDATE()
);

CREATE TABLE Movies (
    MovieID INT PRIMARY KEY IDENTITY(1,1),
    Title NVARCHAR(255),
    ReleaseYear INT,
    Runtime INT,
    Description NVARCHAR(MAX),
    VoteAverage DECIMAL(3, 1) DEFAULT 0.0,
    VoteCount INT DEFAULT 0
);

CREATE TABLE Genres (
    GenreID INT PRIMARY KEY IDENTITY(1,1),
    GenreName NVARCHAR(100) UNIQUE 
);

CREATE TABLE MovieGenres (
    MovieID INT FOREIGN KEY REFERENCES Movies(MovieID),
    GenreID INT FOREIGN KEY REFERENCES Genres(GenreID),
    PRIMARY KEY (MovieID, GenreID)
);

CREATE TABLE Reviews (
    ReviewID INT IDENTITY(1,1),
    UserID INT,
    MovieID INT,
    Rating DECIMAL(3, 1),
    ReviewText NVARCHAR(MAX),
    ReviewDate DATETIME DEFAULT GETDATE() NOT NULL,
    
    CONSTRAINT PK_Reviews PRIMARY KEY NONCLUSTERED (ReviewID, ReviewDate),
    CONSTRAINT FK_Reviews_Users FOREIGN KEY (UserID) REFERENCES Users(UserID),
    CONSTRAINT FK_Reviews_Movies FOREIGN KEY (MovieID) REFERENCES Movies(MovieID)
) ON partition_ReviewDate(ReviewDate); 
GO

CREATE CLUSTERED INDEX CIX_Reviews_Date ON Reviews(ReviewDate) ON partition_ReviewDate(ReviewDate);
GO

CREATE TABLE Watchlist (
    WatchlistID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT FOREIGN KEY REFERENCES Users(UserID),
    MovieID INT FOREIGN KEY REFERENCES Movies(MovieID),
    AddedDate DATETIME DEFAULT GETDATE()
);

CREATE TABLE Follow (
    FollowID INT PRIMARY KEY IDENTITY(1,1),
    FollowerID INT FOREIGN KEY REFERENCES Users(UserID),
    FollowedID INT FOREIGN KEY REFERENCES Users(UserID),
    FollowDate DATETIME DEFAULT GETDATE(),
    CONSTRAINT CK_NoSelfFollow CHECK (FollowerID <> FollowedID),
    CONSTRAINT UK_UniqueFollow UNIQUE (FollowerID, FollowedID)
);

CREATE TABLE Lists (
    ListID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT FOREIGN KEY REFERENCES Users(UserID),
    Title NVARCHAR(100),
    Description NVARCHAR(MAX),
    CreatedDate DATETIME DEFAULT GETDATE()
);

CREATE TABLE ListItem (
    ListItemID INT PRIMARY KEY IDENTITY(1,1),
    ListID INT NOT NULL FOREIGN KEY REFERENCES Lists(ListID),
    MovieID INT NOT NULL FOREIGN KEY REFERENCES Movies(MovieID),
    AddedDate DATETIME DEFAULT GETDATE(),
    CONSTRAINT UQ_ListItem_List_Movie UNIQUE (ListID, MovieID)
);
GO

-- 4. DATA IMPORT & GENERATION

-- A. Import Movies from CSV
IF OBJECT_ID('Staging_Movies', 'U') IS NOT NULL DROP TABLE Staging_Movies;
CREATE TABLE Staging_Movies (
    id NVARCHAR(MAX), title NVARCHAR(MAX), vote_average NVARCHAR(MAX),
    vote_count NVARCHAR(MAX), status NVARCHAR(MAX), release_date NVARCHAR(MAX),
    revenue NVARCHAR(MAX), runtime NVARCHAR(MAX), adult NVARCHAR(MAX),
    backdrop_path NVARCHAR(MAX), budget NVARCHAR(MAX), homepage NVARCHAR(MAX),
    imdb_id NVARCHAR(MAX), original_language NVARCHAR(MAX), original_title NVARCHAR(MAX),
    overview NVARCHAR(MAX), popularity NVARCHAR(MAX), poster_path NVARCHAR(MAX),
    tagline NVARCHAR(MAX), genres NVARCHAR(MAX), production_companies NVARCHAR(MAX),
    production_countries NVARCHAR(MAX), spoken_languages NVARCHAR(MAX), keywords NVARCHAR(MAX)
);
GO

PRINT '1. Bulk Importing Movies...';
BULK INSERT Staging_Movies
FROM '/var/opt/mssql/movies_utf8.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0A',
    KEEPNULLS
);



DELETE FROM Staging_Movies
WHERE title IS NULL
   OR LTRIM(RTRIM(title)) = '';
GO

SELECT *
FROM Staging_Movies
WHERE genres IS NULL
   OR LTRIM(RTRIM(genres)) = '';



-- B. Move Data to Movies Table
PRINT '2. Processing Movies...';
INSERT INTO Movies (Title, ReleaseYear, Runtime, Description, VoteAverage, VoteCount)
SELECT 
    LEFT(title, 255),
    TRY_CAST(LEFT(release_date, 4) AS INT),
    TRY_CAST(runtime AS INT),
    LEFT(overview, 1000),
    TRY_CAST(vote_average AS DECIMAL(3,1)),
    TRY_CAST(vote_count AS INT)
FROM Staging_Movies
WHERE TRY_CAST(LEFT(release_date, 4) AS INT) IS NOT NULL;
GO

-- C. EXTRACT GENRES (New Logic)
PRINT '3. Processing Genres...';

INSERT INTO Genres (GenreName)
SELECT DISTINCT CleanGenre
FROM (
    SELECT NULLIF(LTRIM(RTRIM(value)), '') AS CleanGenre
    FROM Staging_Movies
    CROSS APPLY STRING_SPLIT(genres, ',')
) AS g
WHERE CleanGenre IS NOT NULL
  AND CleanGenre NOT LIKE '%[^a-zA-Z ]%';

INSERT INTO MovieGenres (MovieID, GenreID)
SELECT DISTINCT m.MovieID, g.GenreID
FROM Staging_Movies sm
JOIN Movies m 
    ON sm.title = m.Title
   AND TRY_CAST(LEFT(sm.release_date, 4) AS INT) = m.ReleaseYear
CROSS APPLY (
    SELECT NULLIF(LTRIM(RTRIM(value)), '') AS CleanGenre
    FROM STRING_SPLIT(sm.genres, ',')
) AS split
JOIN Genres g 
    ON split.CleanGenre = g.GenreName
WHERE split.CleanGenre IS NOT NULL;
GO

PRINT '4. Generating Users...';
DECLARE @i INT = 1;
WHILE @i <= 1000
BEGIN
    INSERT INTO Users (UserName, Email) VALUES ('User' + CAST(@i AS NVARCHAR), 'user' + CAST(@i AS NVARCHAR) + '@test.com');
    SET @i = @i + 1;
END
GO

PRINT '5. Generating 1 Million Reviews...';
INSERT INTO Reviews (UserID, MovieID, Rating, ReviewText, ReviewDate)
SELECT TOP (1000000) 
    (ABS(CHECKSUM(NEWID())) % 1000) + 1,
    (ABS(CHECKSUM(NEWID())) % (SELECT COUNT(*) FROM Movies)) + 1,
    (ABS(CHECKSUM(NEWID())) % 50) / 10.0,
    'Auto-generated review for scalability.',
    DATEADD(DAY, - (ABS(CHECKSUM(NEWID())) % 1800), GETDATE())
FROM sys.all_columns a, sys.all_columns b;
GO

PRINT '6. Syncing Movie Ratings...';
WITH CalculatedRatings AS (
    SELECT MovieID, AVG(Rating) as NewAvg, COUNT(*) as NewCount
    FROM Reviews
    GROUP BY MovieID
)
UPDATE m
SET m.VoteAverage = c.NewAvg, m.VoteCount = c.NewCount
FROM Movies m
JOIN CalculatedRatings c ON m.MovieID = c.MovieID;
GO

PRINT '7. Generating Social Data...';
INSERT INTO Follow (FollowerID, FollowedID)
SELECT TOP 2000 u1.UserID, u2.UserID
FROM Users u1 CROSS JOIN Users u2
WHERE u1.UserID <> u2.UserID
ORDER BY NEWID();

INSERT INTO Watchlist (UserID, MovieID)
SELECT TOP 5000
    (ABS(CHECKSUM(NEWID())) % 1000) + 1,
    (ABS(CHECKSUM(NEWID())) % (SELECT COUNT(*) FROM Movies)) + 1
FROM sys.all_columns a, sys.all_columns b;
GO

PRINT '8. Generating Lists and List Items...';

-- Create 3 lists per user (e.g., "eidlist", "Favorites", "Christmas Picks")
DECLARE @u INT = 1;
WHILE @u <= 1000
BEGIN
    INSERT INTO Lists (UserID, Title, Description)
    VALUES 
        (@u, 'Eid Picks of User ' + CAST(@u AS NVARCHAR), 'Auto-generated eidlist'),
        (@u, 'Favorites of User ' + CAST(@u AS NVARCHAR), 'Auto-generated favorites'),
        (@u, 'Christmas Picks of User ' + CAST(@u AS NVARCHAR), 'Auto-generated themed list');
    SET @u = @u + 1;
END

;WITH RandomPairs AS (
    SELECT TOP (20000)
        (ABS(CHECKSUM(NEWID())) % (SELECT COUNT(*) FROM Lists)) + 1 AS ListID,
        (ABS(CHECKSUM(NEWID())) % (SELECT COUNT(*) FROM Movies)) + 1 AS MovieID
    FROM sys.all_columns a, sys.all_columns b
)
INSERT INTO ListItem (ListID, MovieID)
SELECT DISTINCT ListID, MovieID FROM RandomPairs;
GO


-- 5. FEATURE IMPLEMENTATION

-- 5.1 TRIGGERS 

-- Trigger 1: When reviews change, keep Movies.VoteAverage & VoteCount in sync
CREATE TRIGGER trigger_UpdateMovieRating
ON Reviews
AFTER INSERT, DELETE, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @AffectedMovieID INT;

    SELECT TOP 1 @AffectedMovieID = MovieID FROM inserted; 
    IF @AffectedMovieID IS NULL 
        SELECT TOP 1 @AffectedMovieID = MovieID FROM deleted;

    IF @AffectedMovieID IS NOT NULL
    BEGIN
        UPDATE Movies
        SET VoteAverage = (SELECT AVG(Rating) FROM Reviews WHERE MovieID = @AffectedMovieID),
            VoteCount   = (SELECT COUNT(*)   FROM Reviews WHERE MovieID = @AffectedMovieID)
        WHERE MovieID = @AffectedMovieID;
    END
END;
GO

-- Trigger 2: When user reviews a movie, automatically remove it from their Watchlist
CREATE TRIGGER trgger_CleanupWatchlist
ON Reviews
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    DELETE w
    FROM Watchlist w
    JOIN inserted i 
        ON w.UserID = i.UserID 
       AND w.MovieID = i.MovieID;
END;
GO

-- Trigger 3: Prevent future-dated reviews using INSTEAD OF INSERT
CREATE TRIGGER trigger_CheckReviewDate
ON Reviews
INSTEAD OF INSERT
AS
BEGIN
    IF EXISTS (SELECT 1 FROM inserted WHERE ReviewDate > GETDATE())
    BEGIN
        RAISERROR ('Cannot post reviews with a future date.', 16, 1);
    END
    ELSE
    BEGIN
        INSERT INTO Reviews (UserID, MovieID, Rating, ReviewText, ReviewDate)
        SELECT UserID, MovieID, Rating, ReviewText, ReviewDate 
        FROM inserted;
    END
END;
GO

-- 5.2 STORED PROCEDURES 

-- Procedure: Add a review safely (uses current timestamp)
CREATE PROCEDURE proced_AddReview
    @UserID INT, 
    @MovieID INT, 
    @Rating DECIMAL(3, 1), 
    @ReviewText NVARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (SELECT 1 FROM Movies WHERE MovieID = @MovieID)
    BEGIN
        INSERT INTO Reviews (UserID, MovieID, Rating, ReviewText, ReviewDate)
        VALUES (@UserID, @MovieID, @Rating, @ReviewText, GETDATE());
    END
END;
GO

-- Procedure: Follow another user (prevents duplicate follows)
CREATE PROCEDURE proced_FollowUser
    @FollowerID INT, 
    @FollowedID INT
AS
BEGIN
    SET NOCOUNT ON;

    IF NOT EXISTS (
        SELECT 1 
        FROM Follow 
        WHERE FollowerID = @FollowerID 
          AND FollowedID = @FollowedID
    )
    BEGIN
        INSERT INTO Follow (FollowerID, FollowedID) 
        VALUES (@FollowerID, @FollowedID);
    END
END;
GO

-- Procedure: Get users whose review count is above average (already a good analytics feature)
CREATE PROCEDURE proced_GetSuperUsers AS
BEGIN
    SET NOCOUNT ON;

    WITH UserStats AS (
        SELECT UserID, COUNT(*) as TotalReviews 
        FROM Reviews 
        GROUP BY UserID
    ),
    AvgStats AS ( 
        SELECT AVG(TotalReviews) as AvgCount 
        FROM UserStats 
    )
    SELECT u.UserName, s.TotalReviews
    FROM Users u 
    JOIN UserStats s ON u.UserID = s.UserID
    CROSS JOIN AvgStats a 
    WHERE s.TotalReviews > a.AvgCount;
END;
GO

-- Procedure: Find friend-of-friend connections up to 3 levels 
CREATE PROCEDURE proced_FindFriendConnections 
    @StartUserID INT 
AS
BEGIN
    SET NOCOUNT ON;

    WITH FriendGraph AS (
        SELECT FollowerID, FollowedID, 1 AS Level 
        FROM Follow 
        WHERE FollowerID = @StartUserID

        UNION ALL

        SELECT f.FollowerID, f.FollowedID, fg.Level + 1
        FROM Follow f 
        INNER JOIN FriendGraph fg 
            ON f.FollowerID = fg.FollowedID
        WHERE fg.Level < 3
    )
    SELECT DISTINCT u.UserName, fg.Level 
    FROM FriendGraph fg
    JOIN Users u ON fg.FollowedID = u.UserID 
    WHERE fg.FollowedID <> @StartUserID;
END;
GO

-- Procedure: Get all movies for a given genre (for browsing and filters)
CREATE PROCEDURE Proced_GetMoviesByGenre
    @GenreName NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        m.MovieID, 
        m.Title, 
        m.ReleaseYear, 
        m.VoteAverage, 
        m.VoteCount
    FROM Movies m
    JOIN MovieGenres mg ON m.MovieID = mg.MovieID
    JOIN Genres g       ON mg.GenreID = g.GenreID
    WHERE g.GenreName = @GenreName
    ORDER BY m.VoteAverage DESC, m.VoteCount DESC;
END;
GO

-- Procedure: Get consolidated user activity 
CREATE PROCEDURE proced_GetUserActivity
    @UserID INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 'Review' AS ActivityType, m.Title, r.Rating, r.ReviewDate AS ActivityDate
    FROM Reviews r
    JOIN Movies m ON r.MovieID = m.MovieID
    WHERE r.UserID = @UserID

    UNION ALL

    SELECT 'Watchlist', m.Title, NULL, w.AddedDate
    FROM Watchlist w
    JOIN Movies m ON w.MovieID = m.MovieID
    WHERE w.UserID = @UserID

    UNION ALL

    SELECT 'List Item', m.Title, NULL, li.AddedDate
    FROM ListItem li
    JOIN Lists l  ON li.ListID = l.ListID
    JOIN Movies m ON li.MovieID = m.MovieID
    WHERE l.UserID = @UserID
    ORDER BY ActivityDate DESC;
END;
GO

-- Procedure: Get trending movies based on review volume in last @Days
CREATE PROCEDURE proced_GetTrendingMovies
    @Days INT = 30
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        m.MovieID, 
        m.Title, 
        COUNT(*) AS RecentReviews
    FROM Reviews r
    JOIN Movies m ON r.MovieID = m.MovieID
    WHERE r.ReviewDate > DATEADD(DAY, -@Days, GETDATE())
    GROUP BY m.MovieID, m.Title
    ORDER BY RecentReviews DESC, m.Title;
END;
GO

-- Procedure: Simple recommendation based on user's top 3 genres by review count
CREATE PROCEDURE proced_RecommendMovies
    @UserID INT
AS
BEGIN
    SET NOCOUNT ON;

    ;WITH UserGenres AS (
        SELECT TOP 3 g.GenreID
        FROM Reviews r
        JOIN MovieGenres mg ON r.MovieID = mg.MovieID
        JOIN Genres g       ON mg.GenreID = g.GenreID
        WHERE r.UserID = @UserID
        GROUP BY g.GenreID
        ORDER BY COUNT(*) DESC
    )
    SELECT DISTINCT 
        m.MovieID, 
        m.Title, 
        m.ReleaseYear,
        m.VoteAverage,
        m.VoteCount
    FROM Movies m
    JOIN MovieGenres mg ON m.MovieID = mg.MovieID
    WHERE mg.GenreID IN (SELECT GenreID FROM UserGenres)
    ORDER BY m.VoteAverage DESC, m.VoteCount DESC;
END;
GO

-- Procedure: Get full movie details (info + genres + recent reviews)
CREATE PROCEDURE proced_GetMovieDetails
    @MovieID INT
AS
BEGIN
    SET NOCOUNT ON;
    SELECT * 
    FROM Movies 
    WHERE MovieID = @MovieID;
    SELECT g.GenreName
    FROM MovieGenres mg
    JOIN Genres g ON mg.GenreID = g.GenreID
    WHERE mg.MovieID = @MovieID;
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

-- 5.3 FUNCTIONS

-- Function: Count how many reviews a user has posted
CREATE FUNCTION fn_GetUserWatchCount (@UserID INT)
RETURNS INT AS
BEGIN
    DECLARE @Count INT;
    SELECT @Count = COUNT(*) FROM Reviews WHERE UserID = @UserID;
    RETURN @Count;
END;
GO

-- Function: Format runtime (minutes -> "Xh Ym")
CREATE FUNCTION fn_FormatRuntime (@Minutes INT)
RETURNS NVARCHAR(50) AS
BEGIN
    RETURN CAST(@Minutes / 60 AS NVARCHAR) + 'h ' + CAST(@Minutes % 60 AS NVARCHAR) + 'm';
END;
GO

-- Function: Average rating for a given genre (simple analytics helper)
CREATE FUNCTION fn_AvgRatingByGenre (@GenreName NVARCHAR(100))
RETURNS DECIMAL(4,2)
AS
BEGIN
    DECLARE @Avg DECIMAL(4,2);

    SELECT @Avg = AVG(m.VoteAverage)
    FROM MovieGenres mg
    JOIN Genres g ON mg.GenreID = g.GenreID
    JOIN Movies m ON mg.MovieID = m.MovieID
    WHERE g.GenreName = @GenreName;

    RETURN @Avg;
END;
GO

-- 5.4 VIEWS (Predefined query shortcuts)

-- View: Top rated movies with enough votes (for "Top 100" section)
CREATE VIEW vw_TopRatedMovies AS
SELECT TOP 100 
    Title, 
    ReleaseYear, 
    VoteAverage, 
    VoteCount
FROM Movies
WHERE VoteCount > 50
ORDER BY VoteAverage DESC, VoteCount DESC;
GO

-- View: Public recent review feed (for activity timeline)
CREATE VIEW vw_PublicActivityFeed AS
SELECT TOP 50 
    u.UserName, 
    m.Title, 
    r.Rating, 
    r.ReviewText, 
    r.ReviewDate
FROM Reviews r
JOIN Users u ON r.UserID = u.UserID
JOIN Movies m ON r.MovieID = m.MovieID
ORDER BY r.ReviewDate DESC;
GO

-- View: Most active users by review count
CREATE VIEW vw_MostActiveUsers AS
SELECT TOP 50 
    u.UserID,
    u.UserName,
    COUNT(*) AS TotalReviews
FROM Users u
JOIN Reviews r ON u.UserID = r.UserID
GROUP BY u.UserID, u.UserName
ORDER BY TotalReviews DESC;
GO

-- View: Most common genres (by number of movie-genre links)
CREATE VIEW vw_PopularGenres AS
SELECT TOP 20 
    g.GenreName, 
    COUNT(*) AS MovieCount
FROM MovieGenres mg
JOIN Genres g ON mg.GenreID = g.GenreID
GROUP BY g.GenreName
ORDER BY MovieCount DESC, g.GenreName;
GO

-- 5.5 INDEXES (Performance helpers)

CREATE NONCLUSTERED INDEX IX_Movies_Title   ON Movies(Title);
CREATE NONCLUSTERED INDEX IX_Reviews_UserID ON Reviews(UserID);
GO

-- 6. FINAL VERIFICATION
SELECT 'Movies'      as [Table], COUNT(*) as [Rows] FROM Movies
UNION ALL SELECT 'Reviews',     COUNT(*) FROM Reviews
UNION ALL SELECT 'Users',       COUNT(*) FROM Users
UNION ALL SELECT 'Genres',      COUNT(*) FROM Genres
UNION ALL SELECT 'MovieGenres', COUNT(*) FROM MovieGenres;
GO

SELECT * FROM Genres ORDER BY GenreName;

SELECT 'Lists' AS [Table], COUNT(*) AS [Rows] FROM Lists
UNION ALL
SELECT 'ListItem', COUNT(*) FROM ListItem;
GO