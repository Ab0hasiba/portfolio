# Email System Testing Guide

## 🚀 Quick Setup Steps

### 1. Install Python Dependencies
```bash
pip install flask flask-cors requests python-dotenv
```

### 2. Set Up Environment Variables

#### Option A: Using .env file (Recommended for local testing)
Create a `.env` file in your `backend` folder:
```
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
RECIPIENT_EMAIL=your_email@gmail.com
ALLOWED_ORIGIN=*
```

#### Option B: Set environment variables in PowerShell
```powershell
$env:EMAIL_ADDRESS="your_email@gmail.com"
$env:EMAIL_PASSWORD="your_gmail_app_password"
$env:RECIPIENT_EMAIL="your_email@gmail.com"
```

### 3. Gmail App Password Setup
1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account → Security → 2-Step Verification → App passwords
3. Generate a new app password for "Mail"
4. Use this password (not your regular Gmail password)

### 4. Test Your Email System

#### Test 1: Start the Flask Server
```bash
cd backend
python app.py
```

#### Test 2: Test the Endpoint with PowerShell
```powershell
$testData = @{
    name = "Test User"
    email = "test@example.com"
    message = "This is a test message from PowerShell"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/send-email" -Method POST -Body $testData -ContentType "application/json"
    Write-Host "✅ Success: $($response.message)" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}
```

#### Test 3: Test with Browser
1. Open your portfolio in a browser
2. Go to the contact form
3. Fill out the form and submit
4. Check if you receive the email

### 5. Deploy to Render

1. **Push your code to GitHub**
2. **Connect Render to your GitHub repository**
3. **Set environment variables in Render dashboard**:
   - `EMAIL_ADDRESS`: Your Gmail address
   - `EMAIL_PASSWORD`: Your Gmail App Password
   - `RECIPIENT_EMAIL`: Where to receive emails
   - `ALLOWED_ORIGIN`: Your portfolio URL (e.g., https://ab0hasiba.github.io)

### 6. Test Production Deployment

After deploying to Render:
1. Update your frontend to use the Render URL
2. Test the contact form on your live portfolio
3. Check your email for incoming messages

## 🔍 Troubleshooting

### Common Issues:

1. **"Authentication failed"**
   - Make sure you're using Gmail App Password, not regular password
   - Verify 2FA is enabled on your Gmail account

2. **"Connection refused"**
   - Make sure Flask server is running
   - Check if port 5000 is available

3. **"CORS error"**
   - Update ALLOWED_ORIGIN environment variable
   - Make sure your frontend URL is correct

4. **"Module not found"**
   - Install required packages: `pip install flask flask-cors`

### Testing Checklist:
- [ ] Python installed and working
- [ ] Flask dependencies installed
- [ ] Environment variables set
- [ ] Gmail App Password configured
- [ ] Flask server starts without errors
- [ ] Email endpoint responds to test requests
- [ ] Contact form sends emails successfully
- [ ] Emails received in inbox

## 📧 Expected Email Format

When someone submits your contact form, you should receive an email like this:

```
From: Test User <test@example.com>
Subject: New Contact from Test User

Subject: Contact Form Submission

This is a test message from the contact form.
```
