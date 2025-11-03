# GitHub Deployment Guide

This guide walks you through deploying your Grid Analytics Dashboard on GitHub and getting it live.

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and log in
2. Click **"New"** to create a new repository
3. Name it: `grid-analytics-dashboard`
4. Add description: "Grid analytics platform for electricity market data"
5. Choose **Public** (for portfolio) or **Private** (for confidential)
6. Click **"Create repository"**

## Step 2: Initialize Local Repository

```bash
# Navigate to your project directory
cd grid-analytics-dashboard

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Grid Analytics Dashboard with mock API"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/grid-analytics-dashboard.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Deploy Streamlit App on Streamlit Cloud

### 3.1 Create Streamlit Account
- Go to [Streamlit Cloud](https://share.streamlit.io/)
- Sign in with GitHub

### 3.2 Deploy Application
1. Click **"New app"**
2. Select repository: `YOUR_USERNAME/grid-analytics-dashboard`
3. Select branch: `main`
4. Set main file path: `app.py`
5. Click **"Deploy!"**

The app will be live at: `https://YOUR_USERNAME-grid-analytics-dashboard.streamlit.app/`

### 3.3 Add Secrets
1. In Streamlit Cloud dashboard, click on your app
2. Go to **Settings** (gear icon)
3. Under **"Secrets"**, add:

```toml
API_BASE_URL = "http://localhost:5000"
```

Or when using real ERCOT API:
```toml
API_BASE_URL = "https://your-deployed-api.com"
ERCOT_SUBSCRIPTION_KEY = "your_key"
ERCOT_ID_TOKEN = "your_token"
```

## Step 4: Deploy Flask API on Render (Free Option)

### 4.1 Create Render Account
- Go to [Render](https://render.com/)
- Sign up with GitHub

### 4.2 Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `grid-analytics-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn api:app`
4. Click **"Create Web Service"**

Render will provide your API URL: `https://grid-analytics-api-xxxx.onrender.com`

### 4.3 Update Streamlit Secrets
Update your Streamlit Cloud secrets to point to deployed API:
```toml
API_BASE_URL = "https://grid-analytics-api-xxxx.onrender.com"
```

## Step 5: Deploy Flask API on Heroku

Alternatively, use Heroku:

### 5.1 Create Heroku Account
- Go to [Heroku](https://www.heroku.com/)
- Create account

### 5.2 Install Heroku CLI
```bash
# macOS
brew install heroku/brew/heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli

# Verify installation
heroku --version
```

### 5.3 Create Procfile
Create `Procfile` in your project root:
```
web: gunicorn api:app
```

### 5.4 Deploy
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create grid-analytics-api

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

Your API will be at: `https://grid-analytics-api-xxxxx.herokuapp.com`

## Step 6: Deploy on AWS (Advanced)

### 6.1 Create EC2 Instance
1. Go to AWS Console
2. Create EC2 instance (Ubuntu 20.04)
3. Allow ports 5000 (API) and 22 (SSH)

### 6.2 Connect and Deploy
```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Install Python and dependencies
sudo apt update
sudo apt install python3 python3-pip git

# Clone repository
git clone https://github.com/YOUR_USERNAME/grid-analytics-dashboard.git
cd grid-analytics-dashboard

# Install Python packages
pip3 install -r requirements.txt

# Install Gunicorn
pip3 install gunicorn

# Run API
gunicorn -w 4 -b 0.0.0.0:5000 api:app &

# Run Streamlit in background
nohup streamlit run app.py --server.port 8501 > streamlit.log 2>&1 &
```

## Step 7: Set Up Continuous Deployment (CI/CD)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Run tests
      run: |
        pip install -r requirements.txt
        python -m pytest tests/
    
    - name: Deploy to Streamlit Cloud
      # Streamlit Cloud auto-deploys on push to main
      run: echo "Streamlit auto-deploys on git push"
    
    - name: Deploy to Render
      # Render auto-deploys on git push
      run: echo "Render auto-deploys on git push"
```

## Step 8: Monitor Your Deployment

### Check Streamlit App Status
- Visit: `https://YOUR_USERNAME-grid-analytics-dashboard.streamlit.app/`
- Check logs in Streamlit Cloud dashboard

### Check API Status
- Visit: `https://your-api-url.com/api/health`
- Should return: `{"status": "healthy", "timestamp": "..."}`

## Step 9: Update Code and Redeploy

Simply push changes to GitHub:
```bash
git add .
git commit -m "Update: Add new feature"
git push origin main
```

Both Streamlit Cloud and Render will auto-redeploy!

## Troubleshooting

### App shows "App is loading" indefinitely
- Check Streamlit Cloud logs
- Verify requirements.txt is correct
- Ensure app.py is valid Python

### API Connection Error
- Verify API_BASE_URL is correct in secrets
- Check if deployed API is running (`/api/health` endpoint)
- Check CORS is enabled (it is in api.py)

### Missing Dependencies
- Ensure all imports are in requirements.txt
- Redeploy after updating requirements.txt

## Production Checklist

- [ ] Code pushed to GitHub
- [ ] Streamlit app deployed on Streamlit Cloud
- [ ] Flask API deployed on Render/Heroku/AWS
- [ ] Secrets configured correctly
- [ ] API health check passing
- [ ] Dashboard loads without errors
- [ ] All charts and data visible
- [ ] Responsive design works on mobile
- [ ] README updated with deployed URLs
- [ ] Monitoring and alerts set up

## Next Steps

1. **Integrate ERCOT API**: When you have credentials, update your API connector
2. **Add Database**: Store historical data in PostgreSQL/MongoDB
3. **User Authentication**: Add login with GitHub/Google
4. **Advanced Analytics**: Implement machine learning models
5. **Mobile App**: Build React Native companion app

## Support

For deployment issues:
- Check [Streamlit Deployment Docs](https://docs.streamlit.io/streamlit-cloud/get-started)
- Check [Render Documentation](https://render.com/docs)
- Check [Heroku Documentation](https://devcenter.heroku.com/)

---

**Your live dashboard URL will be shared here once deployed! 🎉**
