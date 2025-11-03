# Quick Start Guide

Get your Grid Analytics Dashboard up and running in 5 minutes!

## For Local Development

### Step 1: Clone & Setup (2 minutes)
```bash
git clone https://github.com/yourusername/grid-analytics-dashboard.git
cd grid-analytics-dashboard

# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Create Config (1 minute)
```bash
# Create .streamlit directory
mkdir -p .streamlit

# Create secrets file
cat > .streamlit/secrets.toml << EOF
API_BASE_URL = "http://localhost:5000"
EOF
```

### Step 3: Run Everything (2 minutes)

**Terminal 1 - Start API:**
```bash
python api.py
```
You should see: `📡 API running on http://localhost:5000`

**Terminal 2 - Start Dashboard:**
```bash
streamlit run app.py
```

**Open Browser:**
- Dashboard: `http://localhost:8501`
- API Health: `http://localhost:5000/api/health`

---

## For GitHub Deployment

### Step 1: Push to GitHub (2 minutes)
```bash
git add .
git commit -m "Initial: Grid Analytics Dashboard"
git remote add origin https://github.com/YOUR_USERNAME/grid-analytics-dashboard.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud (3 minutes)
1. Go to [Streamlit Cloud](https://share.streamlit.io/)
2. Click "New app"
3. Select your repository and `app.py`
4. Click "Deploy"
5. Add secrets: `API_BASE_URL = "http://localhost:5000"`

### Step 3: Deploy API on Render (3 minutes)
1. Go to [Render](https://render.com/)
2. Click "New Web Service"
3. Connect your GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn api:app`
6. Deploy!

### Step 4: Connect Them (1 minute)
Update Streamlit Cloud secrets:
```
API_BASE_URL = "https://your-render-api-url.onrender.com"
```

**Done!** Your dashboard is live! 🎉

---

## File Structure

```
grid-analytics-dashboard/
├── app.py                    # 🎨 Streamlit Dashboard
├── api.py                    # ⚡ Flask API Server
├── requirements.txt          # 📦 Dependencies
├── Procfile                  # 🚀 Deployment config
├── .gitignore               # 📝 Git exclusions
├── README.md                # 📖 Documentation
├── DEPLOYMENT.md            # 🌐 Deployment guide
├── QUICKSTART.md            # ⚡ This file
└── .streamlit/
    └── secrets.toml         # 🔐 Local secrets
```

---

## API Endpoints Reference

| Endpoint | Purpose |
|----------|---------|
| `/api/health` | Check API status |
| `/api/lmp` | Get LMP prices |
| `/api/congestion` | Get congestion events |
| `/api/storage` | Get battery status |
| `/api/historical` | Get 24h price history |
| `/api/price-spread` | Get DA-RT spread |
| `/api/ancillary-services` | Get ancillary prices |
| `/api/renewable-generation` | Get wind/solar data |
| `/api/demand-forecast` | Get load forecast |

---

## Dashboard Pages

1. **Dashboard Overview** — Key metrics summary
2. **LMP Analysis** — Price components breakdown
3. **Congestion Monitoring** — Transmission constraints
4. **Energy Storage** — Battery operations
5. **Historical Trends** — 24-hour price history
6. **Price Spread Analysis** — DA vs RT comparison
7. **Settings** — Configuration & documentation

---

## Troubleshooting

### "Connection refused" Error
```
❌ Failed to connect to API
```
**Fix**: Make sure Flask API is running in Terminal 1

### "Module not found" Error
```
❌ ModuleNotFoundError: No module named 'streamlit'
```
**Fix**: `pip install -r requirements.txt`

### App won't load
```
❌ App is loading (stuck)
```
**Fix**: 
- Refresh browser (Ctrl+R)
- Check Streamlit logs
- Verify `app.py` has no syntax errors

### API returning null
```
❌ NoneType error in dashboard
```
**Fix**: 
- Check `/api/health` returns `{"status": "healthy"}`
- Verify API_BASE_URL in secrets
- Restart API server

---

## Next Steps

1. ✅ Explore the dashboard locally
2. ✅ Deploy to GitHub
3. ✅ Test live deployment
4. 🔜 Get ERCOT API credentials
5. 🔜 Integrate real data
6. 🔜 Add database persistence
7. 🔜 Build ML forecasting models
8. 🔜 Create mobile app

---

## Need Help?

📖 **Documentation**: See `README.md` and `DEPLOYMENT.md`
🐛 **Issues**: Open GitHub issue
💬 **Discussions**: Start GitHub discussion
📧 **Contact**: your.email@example.com

---

**Happy analyzing! ⚡📊**
