namespace Phase3
{
    partial class FormLogin
    {
        private System.ComponentModel.IContainer components = null;
        private Label label1;
        private TextBox txtUsername;

        private Button btnLogin;
        private Label lblError;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            label1 = new Label();
            txtUsername = new TextBox();
            btnLogin = new Button();
            lblError = new Label();

            SuspendLayout();

            label1.AutoSize = true;
            label1.Font = new Font("Segoe UI", 16F, FontStyle.Bold, GraphicsUnit.Point);
            label1.Location = new Point(300, 40);
            label1.Text = "CineLog Login";

            txtUsername.Font = new Font("Segoe UI", 11F, FontStyle.Regular, GraphicsUnit.Point);
            txtUsername.Location = new Point(260, 130);
            txtUsername.PlaceholderText = "Enter User ID"; 
            txtUsername.Size = new Size(280, 32);

            lblError.Font = new Font("Segoe UI", 9F, FontStyle.Regular, GraphicsUnit.Point);
            lblError.ForeColor = Color.Red;
            lblError.Location = new Point(260, 170); 
            lblError.Size = new Size(280, 20);
            lblError.Text = "";
            lblError.TextAlign = ContentAlignment.MiddleCenter;

            btnLogin.Font = new Font("Segoe UI", 11F, FontStyle.Bold, GraphicsUnit.Point);
            btnLogin.Location = new Point(320, 200); 
            btnLogin.Size = new Size(150, 45);
            btnLogin.Text = "Login";
            btnLogin.UseVisualStyleBackColor = true;
            btnLogin.Click += btnLogin_Click;

            AutoScaleDimensions = new SizeF(10F, 25F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 450);
            Controls.Add(label1);
            Controls.Add(txtUsername);
            Controls.Add(lblError);
            Controls.Add(btnLogin);
            Name = "FormLogin";
            Text = "Login";

            ResumeLayout(false);
            PerformLayout();
        }
    }
}