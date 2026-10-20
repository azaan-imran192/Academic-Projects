namespace Phase3
{
    partial class Form1
    {
        private System.ComponentModel.IContainer components = null;

        // Main Layout
        private System.Windows.Forms.Panel panelSidebar;
        private System.Windows.Forms.Panel panelHeader;
        private System.Windows.Forms.Panel panelContent;
        private System.Windows.Forms.FlowLayoutPanel flowButtons;

        // Search Controls 
        private System.Windows.Forms.TextBox txtSearch;
        private System.Windows.Forms.Button btnSearch;
        private System.Windows.Forms.Label lblSearch;

        // Other Inputs
        private System.Windows.Forms.ComboBox cboMode;
        private System.Windows.Forms.Label lblMode;
        private System.Windows.Forms.TextBox txtGenre;
        private System.Windows.Forms.Label lblGenre;
        private System.Windows.Forms.TextBox txtMovieId;
        private System.Windows.Forms.Label lblMovieId;
        private System.Windows.Forms.TextBox txtDays;
        private System.Windows.Forms.Label lblDays;
        private System.Windows.Forms.Label lblTitle;

        // Buttons 
        private System.Windows.Forms.Button btnTopRated;
        private System.Windows.Forms.Button btnByGenre;
        private System.Windows.Forms.Button btnDetails;
        private System.Windows.Forms.Button btnTrending;
        private System.Windows.Forms.Button btnRecommend;
        private System.Windows.Forms.Button btnActivity;
        private System.Windows.Forms.Button btnConnections;
        // Dynamic Buttons
        private System.Windows.Forms.Button btnDiary;
        private System.Windows.Forms.Button btnWatchlist;
        private System.Windows.Forms.Button btnLists;
        private System.Windows.Forms.Button btnSuperUsers;
        private System.Windows.Forms.Button btnPopularGenres;
        private System.Windows.Forms.Button btnPublicFeed;

        // Output
        private System.Windows.Forms.DataGridView dgvResults;
        private System.Windows.Forms.Label lblStatus;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null)) components.Dispose();
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        private void InitializeComponent()
        {
            panelSidebar = new System.Windows.Forms.Panel();
            flowButtons = new System.Windows.Forms.FlowLayoutPanel();
            panelHeader = new System.Windows.Forms.Panel();
            panelContent = new System.Windows.Forms.Panel();

            lblTitle = new System.Windows.Forms.Label();
            cboMode = new System.Windows.Forms.ComboBox();
            lblMode = new System.Windows.Forms.Label();
            txtSearch = new System.Windows.Forms.TextBox();
            btnSearch = new System.Windows.Forms.Button();
            lblSearch = new System.Windows.Forms.Label();
            txtGenre = new System.Windows.Forms.TextBox();
            lblGenre = new System.Windows.Forms.Label();
            txtMovieId = new System.Windows.Forms.TextBox();
            lblMovieId = new System.Windows.Forms.Label();
            txtDays = new System.Windows.Forms.TextBox();
            lblDays = new System.Windows.Forms.Label();
            lblStatus = new System.Windows.Forms.Label();
            dgvResults = new System.Windows.Forms.DataGridView();

            btnTopRated = new System.Windows.Forms.Button();
            btnByGenre = new System.Windows.Forms.Button();
            btnDetails = new System.Windows.Forms.Button();
            btnTrending = new System.Windows.Forms.Button();
            btnRecommend = new System.Windows.Forms.Button();
            btnActivity = new System.Windows.Forms.Button();
            btnConnections = new System.Windows.Forms.Button();
            

            ((System.ComponentModel.ISupportInitialize)dgvResults).BeginInit();
            panelSidebar.SuspendLayout();
            panelHeader.SuspendLayout();
            panelContent.SuspendLayout();
            SuspendLayout();

            // --- SIDEBAR ---
            panelSidebar.Dock = System.Windows.Forms.DockStyle.Left;
            panelSidebar.Width = 260;
            panelSidebar.BackColor = System.Drawing.Color.FromArgb(33, 37, 43);
            panelSidebar.Controls.Add(flowButtons);
            panelSidebar.Controls.Add(lblSearch);
            panelSidebar.Controls.Add(txtSearch);
            panelSidebar.Controls.Add(btnSearch);
            panelSidebar.Controls.Add(lblGenre);
            panelSidebar.Controls.Add(txtGenre);
            panelSidebar.Controls.Add(lblMovieId);
            panelSidebar.Controls.Add(txtMovieId);
            panelSidebar.Controls.Add(lblDays);
            panelSidebar.Controls.Add(txtDays);

            lblSearch.Text = "Search Title:";
            lblSearch.ForeColor = System.Drawing.Color.Silver;
            lblSearch.Location = new System.Drawing.Point(12, 15);
            lblSearch.AutoSize = true;

            txtSearch.Location = new System.Drawing.Point(12, 35);
            txtSearch.Size = new System.Drawing.Size(160, 27);

            btnSearch.Text = "Go";
            btnSearch.Location = new System.Drawing.Point(180, 34);
            btnSearch.Size = new System.Drawing.Size(60, 29);
            btnSearch.BackColor = System.Drawing.Color.FromArgb(0, 224, 84); 
            btnSearch.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            btnSearch.Click += btnSearch_Click; 

            int yStart = 80;
            lblGenre.Text = "Genre:";
            lblGenre.ForeColor = System.Drawing.Color.Silver;
            lblGenre.Location = new System.Drawing.Point(12, yStart);
            lblGenre.AutoSize = true;
            txtGenre.Location = new System.Drawing.Point(12, yStart + 20);
            txtGenre.Size = new System.Drawing.Size(228, 27);
            txtGenre.Text = "Action";

            lblMovieId.Text = "Movie ID:";
            lblMovieId.ForeColor = System.Drawing.Color.Silver;
            lblMovieId.Location = new System.Drawing.Point(12, yStart + 60);
            lblMovieId.AutoSize = true;
            txtMovieId.Location = new System.Drawing.Point(12, yStart + 80);
            txtMovieId.Size = new System.Drawing.Size(228, 27);
            txtMovieId.Text = "550";

            lblDays.Text = "Days:";
            lblDays.ForeColor = System.Drawing.Color.Silver;
            lblDays.Location = new System.Drawing.Point(12, yStart + 120);
            lblDays.AutoSize = true;
            txtDays.Location = new System.Drawing.Point(12, yStart + 140);
            txtDays.Size = new System.Drawing.Size(228, 27);
            txtDays.Text = "30";

            flowButtons.Location = new System.Drawing.Point(10, 250);
            flowButtons.Size = new System.Drawing.Size(240, 380);
            flowButtons.FlowDirection = System.Windows.Forms.FlowDirection.TopDown;
            flowButtons.AutoScroll = true;
            flowButtons.WrapContents = false;
            flowButtons.Controls.Add(btnTopRated);
            flowButtons.Controls.Add(btnByGenre);
            flowButtons.Controls.Add(btnDetails);
            flowButtons.Controls.Add(btnTrending);
            flowButtons.Controls.Add(btnRecommend);
            flowButtons.Controls.Add(btnActivity);
            flowButtons.Controls.Add(btnConnections);

            System.Drawing.Size btnSize = new System.Drawing.Size(215, 40);
            System.Drawing.Font btnFont = new System.Drawing.Font("Segoe UI", 10F, System.Drawing.FontStyle.Bold);

            void StyleBtn(System.Windows.Forms.Button b, string t)
            {
                b.Text = t; b.Size = btnSize; b.Font = btnFont; b.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
                b.Margin = new System.Windows.Forms.Padding(0, 0, 0, 5);
            }

            StyleBtn(btnTopRated, "Top Rated");
            btnTopRated.Click += btnTopRated_Click;
            StyleBtn(btnByGenre, "By Genre");
            btnByGenre.Click += btnByGenre_Click;
            StyleBtn(btnDetails, "Movie Details");
            btnDetails.Click += btnDetails_Click;
            StyleBtn(btnTrending, "Trending");
            btnTrending.Click += btnTrending_Click;
            StyleBtn(btnRecommend, "For You");
            btnRecommend.Click += btnRecommend_Click;
            StyleBtn(btnActivity, "User Activity");
            btnActivity.Click += btnActivity_Click;
            StyleBtn(btnConnections, "Friends");
            btnConnections.Click += btnConnections_Click;

            panelHeader.Dock = System.Windows.Forms.DockStyle.Top;
            panelHeader.Height = 80;
            panelHeader.Controls.Add(lblTitle);
            panelHeader.Controls.Add(cboMode);
            panelHeader.Controls.Add(lblMode);

            lblTitle.Text = "CineLog";
            lblTitle.Font = new System.Drawing.Font("Segoe UI", 20F, System.Drawing.FontStyle.Bold);
            lblTitle.Location = new System.Drawing.Point(20, 15);
            lblTitle.AutoSize = true;

            lblMode.Text = "Mode:";
            lblMode.Location = new System.Drawing.Point(600, 30);
            lblMode.AutoSize = true;

            cboMode.Items.AddRange(new object[] { "EF Core", "Stored Procedures" });
            cboMode.Location = new System.Drawing.Point(660, 25);
            cboMode.Size = new System.Drawing.Size(150, 28);
            cboMode.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            cboMode.SelectedIndexChanged += cboMode_SelectedIndexChanged;

            panelContent.Dock = System.Windows.Forms.DockStyle.Fill;
            panelContent.Controls.Add(dgvResults);
            panelContent.Controls.Add(lblStatus);

            dgvResults.Dock = System.Windows.Forms.DockStyle.Fill;
            dgvResults.BackgroundColor = System.Drawing.Color.White;
            dgvResults.BorderStyle = System.Windows.Forms.BorderStyle.None;
            dgvResults.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;

            lblStatus.Dock = System.Windows.Forms.DockStyle.Bottom;
            lblStatus.Height = 30;
            lblStatus.BackColor = System.Drawing.Color.Black;
            lblStatus.ForeColor = System.Drawing.Color.White;
            lblStatus.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            lblStatus.Text = "Ready";

            ClientSize = new System.Drawing.Size(1100, 650);
            Controls.Add(panelContent);
            Controls.Add(panelHeader);
            Controls.Add(panelSidebar);
            Text = "CineLog Phase 3";

            panelSidebar.ResumeLayout(false);
            panelSidebar.PerformLayout();
            panelHeader.ResumeLayout(false);
            panelHeader.PerformLayout();
            panelContent.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)dgvResults).EndInit();
            ResumeLayout(false);
        }

        #endregion
    }
}