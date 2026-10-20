using System;
using System.Collections.Generic;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;
using CineLog.Data.Models;
using CineLog.BLL.DTO;

namespace Phase3
{
    public partial class Form1 : Form
    {
        private readonly Color colorBackground = Color.FromArgb(20, 24, 28);
        private readonly Color colorSidebar = Color.FromArgb(44, 52, 64);
        private readonly Color colorText = Color.FromArgb(230, 230, 230);
        private readonly Color colorAccent = Color.FromArgb(0, 224, 84);
        private readonly Color colorGridHeader = Color.FromArgb(64, 72, 80);

        private int _currentUserId = 0;
        private int _currentListId = 0;

        public event Action<string> SearchClicked;

        public Form1(int userId)
        {
            InitializeComponent();
            _currentUserId = userId;
            lblTitle.Text = $"CineLog (User {_currentUserId})";

            InitializeNewFeatures();

            this.dgvResults.CellClick += dgvResults_CellClick;
            SetupContextMenu();

            ApplyDarkTheme();
            SetupGrid();
        }

        private void InitializeNewFeatures()
        {

            btnWatchlist = new Button();
            btnLists = new Button();
            btnSuperUsers = new Button();
            btnPopularGenres = new Button();
            btnPublicFeed = new Button();


            btnWatchlist.Click += btnWatchlist_Click;
            btnLists.Click += btnLists_Click;
            btnSuperUsers.Click += btnSuperUsers_Click;
            btnPopularGenres.Click += btnPopularGenres_Click;
            btnPublicFeed.Click += btnPublicFeed_Click;


            StyleButton(btnWatchlist, "Watchlist", Color.FromArgb(52, 152, 219));       
            StyleButton(btnLists, "My Lists", Color.FromArgb(155, 89, 182));            
            StyleButton(btnSuperUsers, "Super Users", Color.FromArgb(230, 126, 34));    
            StyleButton(btnPopularGenres, "Popular Genres", Color.FromArgb(192, 57, 43)); 
            StyleButton(btnPublicFeed, "Public Feed", Color.Teal);                      

            StyleButton(btnTopRated, "Top Rated", Color.FromArgb(39, 174, 96));       
            StyleButton(btnByGenre, "By Genre", Color.FromArgb(22, 160, 133));        
            StyleButton(btnDetails, "Movie Details", Color.FromArgb(41, 128, 185));   
            StyleButton(btnTrending, "Trending", Color.FromArgb(243, 156, 18));       
            StyleButton(btnRecommend, "For You", Color.FromArgb(142, 68, 173));       
            StyleButton(btnActivity, "User Activity", Color.FromArgb(52, 73, 94));    
            StyleButton(btnConnections, "Friends", Color.FromArgb(44, 62, 80));       

            AddButtonToFlow(btnPublicFeed);
            AddButtonToFlow(btnWatchlist);
            AddButtonToFlow(btnLists);

            Label divider = new Label { Text = "Analytics", ForeColor = Color.Gray, AutoSize = true, Padding = new Padding(0, 10, 0, 5) };

            bool hasDivider = false;
            foreach (Control c in flowButtons.Controls) if (c is Label && c.Text == "Analytics") hasDivider = true;

            if (!hasDivider) flowButtons.Controls.Add(divider);

            AddButtonToFlow(btnSuperUsers);
            AddButtonToFlow(btnPopularGenres);
        }

        private void AddButtonToFlow(Button btn)
        {
            var existing = flowButtons.Controls.OfType<Button>().FirstOrDefault(b => b.Text == btn.Text);
            if (existing != null) flowButtons.Controls.Remove(existing);

            flowButtons.Controls.Add(btn);
        }

        private void StyleButton(Button btn, string text, Color color)
        {
            if (btn == null) return;
            btn.Text = text;
            btn.BackColor = color;
            btn.ForeColor = Color.White;
            btn.FlatStyle = FlatStyle.Flat;
            btn.FlatAppearance.BorderSize = 0;

            if (btn != btnSearch)
            {
                btn.Size = new Size(215, 50);
                btn.Margin = new Padding(0, 0, 0, 5);
            }

            btn.Font = new Font("Segoe UI", 10F, FontStyle.Bold);
            btn.Cursor = Cursors.Hand;
        }

        private string ShowInputDialog(string text, string caption)
        {
            Form prompt = new Form()
            {
                Width = 400,
                Height = 180,
                FormBorderStyle = FormBorderStyle.FixedDialog,
                Text = caption,
                StartPosition = FormStartPosition.CenterScreen
            };
            Label textLabel = new Label() { Left = 20, Top = 20, Text = text, AutoSize = true };
            TextBox textBox = new TextBox() { Left = 20, Top = 50, Width = 340 };
            Button confirmation = new Button() { Text = "Ok", Left = 260, Width = 100, Top = 90, DialogResult = DialogResult.OK };

            prompt.Controls.Add(textLabel);
            prompt.Controls.Add(textBox);
            prompt.Controls.Add(confirmation);
            prompt.AcceptButton = confirmation;

            return prompt.ShowDialog() == DialogResult.OK ? textBox.Text : "";
        }

        // --- CONTEXT MENU ---
        private void SetupContextMenu()
        {
            ContextMenuStrip ctxMenu = new ContextMenuStrip();

            // 1. WATCHLIST OPERATIONS
            ToolStripMenuItem itemWatchAdd = new ToolStripMenuItem("Add to Watchlist");
            itemWatchAdd.Click += async (s, e) => {
                if (int.TryParse(txtMovieId.Text, out int m))
                {
                    try { await ApiClient.AddToWatchlistAsync(_currentUserId, m); ShowStatus("Added to Watchlist!"); }
                    catch { ShowStatus("Failed (Already in list?)."); }
                }
            };

            ToolStripMenuItem itemWatchRemove = new ToolStripMenuItem("Remove from Watchlist");
            itemWatchRemove.Click += async (s, e) => {
                if (int.TryParse(txtMovieId.Text, out int m))
                {
                    try { await ApiClient.RemoveFromWatchlistAsync(_currentUserId, m); ShowStatus("Removed."); btnWatchlist.PerformClick(); }
                    catch { ShowStatus("Failed to remove."); }
                }
            };

            // 2. REVIEWS 
            ToolStripMenuItem itemReview = new ToolStripMenuItem("Write a Review");
            itemReview.Click += async (s, e) => {
                if (int.TryParse(txtMovieId.Text, out int m))
                {
                    string ratingStr = ShowInputDialog("Enter Rating (1-10):", "Rate Movie");
                    if (!int.TryParse(ratingStr, out int rating) || rating < 1 || rating > 10)
                    {
                        MessageBox.Show("Invalid rating. Must be 1-10."); return;
                    }

                    string comment = ShowInputDialog("Write your review:", "Review Text");
                    if (string.IsNullOrWhiteSpace(comment)) return;

                    try
                    {
                        await ApiClient.AddReviewAsync(_currentUserId, m, rating, comment);
                        ShowStatus("Review posted successfully!");
                    }
                    catch (Exception ex) { ShowStatus("Review failed: " + ex.Message); }
                }
            };

            // 3. CUSTOM LIST OPERATIONS
            ToolStripMenuItem itemListAdd = new ToolStripMenuItem("Add to Current List");
            itemListAdd.Click += async (s, e) => {
                if (_currentListId == 0) { ShowStatus("Open a list first (Click 'My Lists' -> Right Click a list -> Open)."); return; }
                if (int.TryParse(txtMovieId.Text, out int m))
                {
                    try { await ApiClient.AddListItemAsync(_currentListId, m); ShowStatus($"Added to List #{_currentListId}!"); }
                    catch { ShowStatus("Failed to add."); }
                }
            };

            ToolStripMenuItem itemListRemove = new ToolStripMenuItem("Remove from Current List");
            itemListRemove.Click += async (s, e) => {
                if (_currentListId == 0) return;
                if (int.TryParse(txtMovieId.Text, out int m))
                {
                    try { await ApiClient.RemoveListItemAsync(_currentListId, m); ShowStatus("Removed."); ReloadCurrentList(); }
                    catch { ShowStatus("Failed to remove."); }
                }
            };

            // 4. NAVIGATION & CREATION
            ToolStripMenuItem itemOpenList = new ToolStripMenuItem("Open Selected List");
            itemOpenList.Click += (s, e) => {
                if (dgvResults.SelectedRows.Count > 0)
                {
                    var row = dgvResults.SelectedRows[0];
                    if (dgvResults.Columns.Contains("ListId") && row.Cells["ListId"].Value != null)
                    {
                        _currentListId = (int)row.Cells["ListId"].Value;
                        ReloadCurrentList();
                    }
                    else { ShowStatus("Select a List row first."); }
                }
            };

            ToolStripMenuItem itemCreateList = new ToolStripMenuItem("Create New List");
            itemCreateList.Click += async (s, e) => {
                string name = ShowInputDialog("Enter List Name:", "New List");
                if (!string.IsNullOrWhiteSpace(name))
                {
                    try { await ApiClient.CreateListAsync(_currentUserId, name, "User List"); ShowStatus("List Created!"); btnLists.PerformClick(); }
                    catch { ShowStatus("Failed."); }
                }
            };

            ToolStripMenuItem itemFriendActivity = new ToolStripMenuItem("View Friend's Activity");
            itemFriendActivity.Click += async (s, e) => {
                if (int.TryParse(txtMovieId.Text, out int friendId))
                {
                    ShowStatus($"Loading activity for Friend #{friendId}...");
                    try
                    {
                        var activity = await ApiClient.GetUserActivityAsync(friendId);
                        DisplayData<UserActivityDTO>(activity);
                        ShowStatus($"Viewing activity for Friend #{friendId}.");
                    }
                    catch (Exception ex) { ShowStatus("Failed to load activity: " + ex.Message); }
                }
            };

            ctxMenu.Items.Add(new ToolStripSeparator());
            ctxMenu.Items.Add(itemFriendActivity); 
            ctxMenu.Items.Add(itemWatchAdd);
            ctxMenu.Items.Add(itemWatchRemove);
            ctxMenu.Items.Add(new ToolStripSeparator());
            ctxMenu.Items.Add(itemReview);
            ctxMenu.Items.Add(new ToolStripSeparator());
            ctxMenu.Items.Add(itemListAdd);
            ctxMenu.Items.Add(itemListRemove);
            ctxMenu.Items.Add(new ToolStripSeparator());
            ctxMenu.Items.Add(itemOpenList);
            ctxMenu.Items.Add(itemCreateList);

            dgvResults.ContextMenuStrip = ctxMenu;
        }

        private async void ReloadCurrentList()
        {
            if (_currentListId == 0) return;
            ShowStatus($"Loading List #{_currentListId}...");
            try
            {
                var movies = await ApiClient.GetListItemsAsync(_currentListId);
                DisplayData<Movie>(movies);
            }
            catch { ShowStatus("Failed to load list."); }
        }

        // --- EVENTS ---
        private void dgvResults_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            if (e.RowIndex < 0) return;

            var row = dgvResults.Rows[e.RowIndex];
            string id = null;

            if (dgvResults.Columns.Contains("MovieId") && row.Cells["MovieId"].Value != null)
            {
                id = row.Cells["MovieId"].Value.ToString();
                txtMovieId.Text = id;
                ShowStatus($"Selected Movie ID: {id}");
            }
            else if (dgvResults.Columns.Contains("MovieID") && row.Cells["MovieID"].Value != null)
            {
                id = row.Cells["MovieID"].Value.ToString();
                txtMovieId.Text = id;
                ShowStatus($"Selected Movie ID: {id}");
            }

            else if (dgvResults.Columns.Contains("ListId") && row.Cells["ListId"].Value != null)
            {
                int listId = Convert.ToInt32(row.Cells["ListId"].Value);
                _currentListId = listId;

                txtMovieId.Text = listId.ToString();
                ShowStatus($"Selected List #{listId}. Right-click and choose 'Open This List' to view contents.");
            }

            else if (dgvResults.Columns.Contains("FriendId") && row.Cells["FriendId"].Value != null)
            {
                id = row.Cells["FriendId"].Value.ToString();
                txtMovieId.Text = id; 
                ShowStatus($"Selected Friend #{id}. Right-click to View Activity.");
                return;
            }
            else if (dgvResults.Columns.Contains("UserId") && row.Cells["UserId"].Value != null)
            {
                id = row.Cells["UserId"].Value.ToString();
                txtMovieId.Text = id;
                ShowStatus($"Selected User #{id}. Right-click to View Activity.");
                return;
            }

            if (!string.IsNullOrEmpty(id))
            {
                txtMovieId.Text = id;
                ShowStatus($"Selected Movie {id}");
            }
        }
        // --- BUTTON HANDLERS ---
        private async void btnLists_Click(object sender, EventArgs e)
        {
            _currentListId = 0;
            try { DisplayData<List>(await ApiClient.GetUserListsAsync(_currentUserId)); ShowStatus("Your Lists."); }
            catch (Exception ex) { ShowStatus(ex.Message); }
        }

        private async void btnWatchlist_Click(object sender, EventArgs e)
        {
            _currentListId = 0;
            try { DisplayData<Movie>(await ApiClient.GetWatchlistAsync(_currentUserId)); } catch (Exception ex) { ShowStatus(ex.Message); }
        }

        private async void btnSearch_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(txtSearch.Text)) return;
            try { DisplayData<Movie>(await ApiClient.SearchMoviesAsync(txtSearch.Text)); } catch (Exception ex) { ShowStatus(ex.Message); }
        }

        private async void btnPublicFeed_Click(object sender, EventArgs e) { try { DisplayData<ActivityFeedDTO>(await ApiClient.GetPublicFeedAsync()); } catch (Exception ex) { ShowStatus(ex.Message); } }
        private async void btnSuperUsers_Click(object sender, EventArgs e) { try { DisplayData<SuperUserDTO>(await ApiClient.GetSuperUsersAsync()); } catch (Exception ex) { ShowStatus(ex.Message); } }
        private async void btnPopularGenres_Click(object sender, EventArgs e) { try { DisplayData<PopularGenreDTO>(await ApiClient.GetPopularGenresAsync()); } catch (Exception ex) { ShowStatus(ex.Message); } }
        private async void btnTopRated_Click(object sender, EventArgs e) { try { DisplayData<VwTopRatedMovie>(await ApiClient.GetTopRatedAsync()); } catch (Exception ex) { ShowStatus(ex.Message); } }
        private async void btnByGenre_Click(object sender, EventArgs e) { try { DisplayData<Movie>(await ApiClient.GetMoviesByGenreAsync(txtGenre.Text)); } catch (Exception ex) { ShowStatus(ex.Message); } }

        private async void btnDetails_Click(object sender, EventArgs e)
        {
            if (int.TryParse(txtMovieId.Text, out int m))
            {
                try
                {
                    var d = await ApiClient.GetMovieDetailsAsync(m);
                    if (d != null)
                    {
                        DataTable dt = new DataTable(); dt.Columns.Add("Attribute"); dt.Columns.Add("Value");
                        dt.Rows.Add("Title", d.Title);
                        dt.Rows.Add("Rating", d.VoteAverage);
                        foreach (var r in d.RecentReviews) dt.Rows.Add("Review", $"{r.Rating}★ {r.ReviewText}");
                        dgvResults.DataSource = dt;
                    }
                }
                catch (Exception ex) { ShowStatus(ex.Message); }
            }
        }
        private async void btnTrending_Click(object sender, EventArgs e) { if (int.TryParse(txtDays.Text, out int d)) try { DisplayData<Movie>(await ApiClient.GetTrendingAsync(d)); } catch (Exception ex) { ShowStatus(ex.Message); } }
        private async void btnRecommend_Click(object sender, EventArgs e) { try { DisplayData<Movie>(await ApiClient.RecommendMoviesAsync(_currentUserId)); } catch (Exception ex) { ShowStatus(ex.Message); } }
        private async void btnActivity_Click(object sender, EventArgs e) { try { DisplayData<UserActivityDTO>(await ApiClient.GetUserActivityAsync(_currentUserId)); } catch (Exception ex) { ShowStatus(ex.Message); } }
        private async void btnConnections_Click(object sender, EventArgs e) { try { DisplayData<FriendConnectionDTO>(await ApiClient.GetFriendConnectionsAsync(_currentUserId)); } catch (Exception ex) { ShowStatus(ex.Message); } }

        private void cboMode_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (cboMode.SelectedItem == null) return;
            string m = cboMode.SelectedItem.ToString().Contains("Stored") ? "sp" : "ef";
            _ = ApiClient.SetModeAsync(m); ShowStatus("Mode: " + m);
        }

        // --- HELPERS ---
        private void DisplayData<T>(IEnumerable<T> data)
        {
            if (data == null || !data.Any()) { dgvResults.DataSource = null; ShowStatus("No results."); return; }
            DataTable dt = new DataTable();
            foreach (var p in typeof(T).GetProperties()) dt.Columns.Add(p.Name, Nullable.GetUnderlyingType(p.PropertyType) ?? p.PropertyType);
            foreach (var item in data)
            {
                var values = new object[typeof(T).GetProperties().Length];
                for (int i = 0; i < values.Length; i++) values[i] = typeof(T).GetProperties()[i].GetValue(item) ?? DBNull.Value;
                dt.Rows.Add(values);
            }
            dgvResults.DataSource = dt;
            ShowStatus($"Loaded {dt.Rows.Count} rows.");
        }
        private void ApplyDarkTheme()
        {
            this.BackColor = colorBackground; panelSidebar.BackColor = colorSidebar; panelHeader.BackColor = colorSidebar; panelContent.BackColor = colorBackground;
            lblTitle.ForeColor = colorText; lblStatus.ForeColor = Color.Gray;
            foreach (Control c in panelSidebar.Controls) { if (c is TextBox t) { t.BackColor = Color.FromArgb(60, 70, 80); t.ForeColor = Color.White; t.BorderStyle = BorderStyle.FixedSingle; } if (c is Label l) l.ForeColor = Color.Silver; }
        }
        private void SetupGrid()
        {
            dgvResults.BackgroundColor = colorBackground; dgvResults.BorderStyle = BorderStyle.None;
            dgvResults.DefaultCellStyle.BackColor = colorBackground; dgvResults.DefaultCellStyle.ForeColor = colorText;
            dgvResults.ColumnHeadersDefaultCellStyle.BackColor = colorGridHeader; dgvResults.ColumnHeadersDefaultCellStyle.ForeColor = colorText;
            dgvResults.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill; dgvResults.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
        }
        private void ShowStatus(string msg) => lblStatus.Text = msg;
    }
}