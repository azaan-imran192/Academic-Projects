using System;
using System.Drawing;
using System.Net.Http;
using System.Windows.Forms;

namespace Phase3
{
    public partial class FormLogin : Form
    {
        public FormLogin()
        {
            InitializeComponent();
            ApplyStyles();
        }

        private void ApplyStyles()
        {
            this.BackColor = Color.FromArgb(20, 24, 28);

            label1.ForeColor = Color.White;
            lblError.ForeColor = Color.FromArgb(231, 76, 60);

            StyleInput(txtUsername);
            txtUsername.PlaceholderText = "User ID (e.g. 1)"; 

            btnLogin.BackColor = Color.FromArgb(0, 224, 84); 
            btnLogin.ForeColor = Color.Black; 
            btnLogin.FlatStyle = FlatStyle.Flat;
            btnLogin.FlatAppearance.BorderSize = 0;
            btnLogin.Cursor = Cursors.Hand;
        }

        private void StyleInput(TextBox txt)
        {
            txt.BackColor = Color.FromArgb(44, 52, 64);
            txt.ForeColor = Color.White;
            txt.BorderStyle = BorderStyle.FixedSingle;
        }

        private async void btnLogin_Click(object sender, EventArgs e)
        {
            lblError.Text = "";

            if (!int.TryParse(txtUsername.Text.Trim(), out int userId))
            {
                lblError.Text = "User ID must be a number.";
                return;
            }

            try
            {
                var activity = await ApiClient.GetUserActivityAsync(userId);

                Form1 main = new Form1(userId);
                main.Show();
                this.Hide();
            }
            catch (HttpRequestException ex)
            {
                if (ex.StatusCode == System.Net.HttpStatusCode.NotFound)
                {
                    lblError.Text = $"Login failed: User ID {userId} not found.";
                }
                else
                {
                    lblError.Text = $"API Error: {ex.Message}. Check backend status.";
                }
            }
            catch (Exception ex)
            {
                lblError.Text = $"An unexpected error occurred: {ex.Message}";
            }
        }
    }
}