//using Microsoft.EntityFrameworkCore;
//using System;
//using System.Collections.Generic;
//using System.Reflection.Emit;


//namespace CineLog.Data.Models
//{
//    public partial class CineLogContext : DbContext
//    {
//        public CineLogContext(DbContextOptions<CineLogContext> options)
//            : base(options)
//        {
//        }

//        public virtual DbSet<Follow> Follows { get; set; }
//        public virtual DbSet<Genre> Genres { get; set; }
//        public virtual DbSet<List> Lists { get; set; }
//        public virtual DbSet<ListItem> ListItems { get; set; }
//        public virtual DbSet<Movie> Movies { get; set; }
//        public virtual DbSet<Review> Reviews { get; set; }
//        public virtual DbSet<StagingMovie> StagingMovies { get; set; }
//        public virtual DbSet<User> Users { get; set; }
//        public virtual DbSet<VwMostActiveUser> VwMostActiveUsers { get; set; }
//        public virtual DbSet<VwPopularGenre> VwPopularGenres { get; set; }
//        public virtual DbSet<VwPublicActivityFeed> VwPublicActivityFeeds { get; set; }
//        public virtual DbSet<VwTopRatedMovie> VwTopRatedMovies { get; set; }
//        public virtual DbSet<Watchlist> Watchlists { get; set; }



//        protected override void OnModelCreating(ModelBuilder modelBuilder)
//        {
//            modelBuilder.Entity<Follow>(entity =>
//            {
//                entity.HasKey(e => e.FollowId).HasName("PK__Follow__2CE8108E73A0E41C");

//                entity.ToTable("Follow");

//                entity.HasIndex(e => new { e.FollowerId, e.FollowedId }, "UK_UniqueFollow").IsUnique();

//                entity.Property(e => e.FollowId).HasColumnName("FollowID");
//                entity.Property(e => e.FollowDate)
//                    .HasDefaultValueSql("(getdate())")
//                    .HasColumnType("datetime");
//                entity.Property(e => e.FollowedId).HasColumnName("FollowedID");
//                entity.Property(e => e.FollowerId).HasColumnName("FollowerID");

//                entity.HasOne(d => d.Followed).WithMany(p => p.FollowFolloweds)
//                    .HasForeignKey(d => d.FollowedId)
//                    .HasConstraintName("FK__Follow__Followed__5070F446");

//                entity.HasOne(d => d.Follower).WithMany(p => p.FollowFollowers)
//                    .HasForeignKey(d => d.FollowerId)
//                    .HasConstraintName("FK__Follow__Follower__4F7CD00D");
//            });

//            modelBuilder.Entity<Genre>(entity =>
//            {
//                entity.HasKey(e => e.GenreId).HasName("PK__Genres__0385055EA09FF52C");

//                entity.HasIndex(e => e.GenreName, "UQ__Genres__BBE1C3391BD78460").IsUnique();

//                entity.Property(e => e.GenreId).HasColumnName("GenreID");
//                entity.Property(e => e.GenreName).HasMaxLength(100);
//            });

//            modelBuilder.Entity<List>(entity =>
//            {
//                entity.HasKey(e => e.ListId).HasName("PK__Lists__E3832865CE3E5FA9");

//                entity.Property(e => e.ListId).HasColumnName("ListID");
//                entity.Property(e => e.CreatedDate)
//                    .HasDefaultValueSql("(getdate())")
//                    .HasColumnType("datetime");
//                entity.Property(e => e.Title).HasMaxLength(100);
//                entity.Property(e => e.UserId).HasColumnName("UserID");

//                entity.HasOne(d => d.User).WithMany(p => p.Lists)
//                    .HasForeignKey(d => d.UserId)
//                    .HasConstraintName("FK__Lists__UserID__5535A963");
//            });

//            modelBuilder.Entity<ListItem>(entity =>
//            {
//                entity.HasKey(e => e.ListItemId).HasName("PK__ListItem__D93C6967705639C6");

//                entity.ToTable("ListItem");

//                entity.HasIndex(e => new { e.ListId, e.MovieId }, "UQ_ListItem_List_Movie").IsUnique();

//                entity.Property(e => e.ListItemId).HasColumnName("ListItemID");
//                entity.Property(e => e.AddedDate)
//                    .HasDefaultValueSql("(getdate())")
//                    .HasColumnType("datetime");
//                entity.Property(e => e.ListId).HasColumnName("ListID");
//                entity.Property(e => e.MovieId).HasColumnName("MovieID");

//                entity.HasOne(d => d.List).WithMany(p => p.ListItems)
//                    .HasForeignKey(d => d.ListId)
//                    .OnDelete(DeleteBehavior.ClientSetNull)
//                    .HasConstraintName("FK__ListItem__ListID__59FA5E80");

//                entity.HasOne(d => d.Movie).WithMany(p => p.ListItems)
//                    .HasForeignKey(d => d.MovieId)
//                    .OnDelete(DeleteBehavior.ClientSetNull)
//                    .HasConstraintName("FK__ListItem__MovieI__5AEE82B9");
//            });

//            modelBuilder.Entity<Movie>(entity =>
//            {
//                entity.HasKey(e => e.MovieId).HasName("PK__Movies__4BD2943A0588A005");

//                entity.HasIndex(e => e.Title, "IX_Movies_Title");

//                entity.Property(e => e.MovieId).HasColumnName("MovieID");
//                entity.Property(e => e.Title).HasMaxLength(255);
//                entity.Property(e => e.VoteAverage)
//                    .HasDefaultValue(0.0m)
//                    .HasColumnType("decimal(3, 1)");
//                entity.Property(e => e.VoteCount).HasDefaultValue(0);

//                entity.HasMany(d => d.Genres).WithMany(p => p.Movies)
//                    .UsingEntity<Dictionary<string, object>>(
//                        "MovieGenre",
//                        r => r.HasOne<Genre>().WithMany()
//                            .HasForeignKey("GenreId")
//                            .OnDelete(DeleteBehavior.ClientSetNull)
//                            .HasConstraintName("FK__MovieGenr__Genre__4222D4EF"),
//                        l => l.HasOne<Movie>().WithMany()
//                            .HasForeignKey("MovieId")
//                            .OnDelete(DeleteBehavior.ClientSetNull)
//                            .HasConstraintName("FK__MovieGenr__Movie__412EB0B6"),
//                        j =>
//                        {
//                            j.HasKey("MovieId", "GenreId").HasName("PK__MovieGen__BBEAC46F5F39FF03");
//                            j.ToTable("MovieGenres");
//                            j.IndexerProperty<int>("MovieId").HasColumnName("MovieID");
//                            j.IndexerProperty<int>("GenreId").HasColumnName("GenreID");
//                        });
//            });

//            modelBuilder.Entity<Review>(entity =>
//            {
//                entity.HasKey(e => new { e.ReviewId, e.ReviewDate }).IsClustered(false);

//                entity.ToTable(tb =>
//                {
//                    tb.HasTrigger("trgger_CleanupWatchlist");
//                    tb.HasTrigger("trigger_CheckReviewDate");
//                    tb.HasTrigger("trigger_UpdateMovieRating");
//                });

//                entity.HasIndex(e => e.ReviewDate, "CIX_Reviews_Date").IsClustered();
//                entity.HasIndex(e => new { e.ReviewDate, e.UserId }, "IX_Reviews_UserID");

//                entity.Property(e => e.ReviewId)
//                    .ValueGeneratedOnAdd()
//                    .HasColumnName("ReviewID");
//                entity.Property(e => e.ReviewDate)
//                    .HasDefaultValueSql("(getdate())")
//                    .HasColumnType("datetime");
//                entity.Property(e => e.MovieId).HasColumnName("MovieID");
//                entity.Property(e => e.Rating).HasColumnType("decimal(3, 1)");
//                entity.Property(e => e.UserId).HasColumnName("UserID");

//                entity.HasOne(d => d.Movie).WithMany(p => p.Reviews)
//                    .HasForeignKey(d => d.MovieId)
//                    .HasConstraintName("FK_Reviews_Movies");

//                entity.HasOne(d => d.User).WithMany(p => p.Reviews)
//                    .HasForeignKey(d => d.UserId)
//                    .HasConstraintName("FK_Reviews_Users");
//            });

//            modelBuilder.Entity<StagingMovie>(entity =>
//            {
//                entity.HasNoKey().ToTable("Staging_Movies");

//                entity.Property(e => e.Adult).HasColumnName("adult");
//                entity.Property(e => e.BackdropPath).HasColumnName("backdrop_path");
//                entity.Property(e => e.Budget).HasColumnName("budget");
//                entity.Property(e => e.Genres).HasColumnName("genres");
//                entity.Property(e => e.Homepage).HasColumnName("homepage");
//                entity.Property(e => e.Id).HasColumnName("id");
//                entity.Property(e => e.ImdbId).HasColumnName("imdb_id");
//                entity.Property(e => e.Keywords).HasColumnName("keywords");
//                entity.Property(e => e.OriginalLanguage).HasColumnName("original_language");
//                entity.Property(e => e.OriginalTitle).HasColumnName("original_title");
//                entity.Property(e => e.Overview).HasColumnName("overview");
//                entity.Property(e => e.Popularity).HasColumnName("popularity");
//                entity.Property(e => e.PosterPath).HasColumnName("poster_path");
//                entity.Property(e => e.ProductionCompanies).HasColumnName("production_companies");
//                entity.Property(e => e.ProductionCountries).HasColumnName("production_countries");
//                entity.Property(e => e.ReleaseDate).HasColumnName("release_date");
//                entity.Property(e => e.Revenue).HasColumnName("revenue");
//                entity.Property(e => e.Runtime).HasColumnName("runtime");
//                entity.Property(e => e.SpokenLanguages).HasColumnName("spoken_languages");
//                entity.Property(e => e.Status).HasColumnName("status");
//                entity.Property(e => e.Tagline).HasColumnName("tagline");
//                entity.Property(e => e.Title).HasColumnName("title");
//                entity.Property(e => e.VoteAverage).HasColumnName("vote_average");
//                entity.Property(e => e.VoteCount).HasColumnName("vote_count");
//            });

//            modelBuilder.Entity<User>(entity =>
//            {
//                entity.HasKey(e => e.UserId).HasName("PK__Users__1788CCACF2A0B93B");

//                entity.Property(e => e.UserId).HasColumnName("UserID");
//                entity.Property(e => e.Email).HasMaxLength(100);
//                entity.Property(e => e.JoinDate)
//                    .HasDefaultValueSql("(getdate())")
//                    .HasColumnType("datetime");
//                entity.Property(e => e.UserName).HasMaxLength(100);
//            });

//            modelBuilder.Entity<VwMostActiveUser>(entity =>
//            {
//                entity.HasNoKey().ToView("vw_MostActiveUsers");
//                entity.Property(e => e.UserId).HasColumnName("UserID");
//                entity.Property(e => e.UserName).HasMaxLength(100);
//            });

//            modelBuilder.Entity<VwPopularGenre>(entity =>
//            {
//                entity.HasNoKey().ToView("vw_PopularGenres");
//                entity.Property(e => e.GenreName).HasMaxLength(100);
//            });

//            modelBuilder.Entity<VwPublicActivityFeed>(entity =>
//            {
//                entity.HasNoKey().ToView("vw_PublicActivityFeed");
//                entity.Property(e => e.Rating).HasColumnType("decimal(3, 1)");
//                entity.Property(e => e.ReviewDate).HasColumnType("datetime");
//                entity.Property(e => e.Title).HasMaxLength(255);
//                entity.Property(e => e.UserName).HasMaxLength(100);
//            });

//            modelBuilder.Entity<VwTopRatedMovie>(entity =>
//            {
//                entity.HasNoKey().ToView("vw_TopRatedMovies");
//                entity.Property(e => e.Title).HasMaxLength(255);
//                entity.Property(e => e.VoteAverage).HasColumnType("decimal(3, 1)");
//            });

//            modelBuilder.Entity<Watchlist>(entity =>
//            {
//                entity.HasKey(e => e.WatchlistId).HasName("PK__Watchlis__48DEAA2B67DF96F6");

//                entity.ToTable("Watchlist");

//                entity.Property(e => e.WatchlistId).HasColumnName("WatchlistID");
//                entity.Property(e => e.AddedDate)
//                    .HasDefaultValueSql("(getdate())")
//                    .HasColumnType("datetime");
//                entity.Property(e => e.MovieId).HasColumnName("MovieID");
//                entity.Property(e => e.UserId).HasColumnName("UserID");

//                entity.HasOne(d => d.Movie).WithMany(p => p.Watchlists)
//                    .HasForeignKey(d => d.MovieId)
//                    .HasConstraintName("FK__Watchlist__Movie__4AB81AF0");

//                entity.HasOne(d => d.User).WithMany(p => p.Watchlists)
//                    .HasForeignKey(d => d.UserId)
//                    .HasConstraintName("FK__Watchlist__UserI__49C3F6B7");
//            });





//            OnModelCreatingPartial(modelBuilder);
//        }

//        partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
//    }
//}