# Grid Analytics & LMP Dashboard

A comprehensive web-based grid analytics platform for monitoring electricity grid operations, analyzing Locational Marginal Prices (LMP), tracking congestion, and managing energy storage. Built with Streamlit and Flask.

## 🚀 Features

- **Real-Time LMP Analysis**: Visualize Locational Marginal Prices with decomposed components (Energy, Congestion, Loss)
- **Congestion Monitoring**: Track transmission constraints and identify bottlenecks
- **Energy Storage Tracking**: Monitor battery charge/discharge operations
- **Historical Analysis**: 24-hour price trends and patterns
- **Price Spread Visualization**: Day-Ahead vs Real-Time price comparison
- **Ancillary Services**: Monitor battery participation in grid support services
- **Renewable Generation**: Track wind and solar output
- **Demand Forecasting**: View load forecasts for next 24 hours
- **Interactive Dashboards**: Built with Plotly for rich interactivity

## 📋 Prerequisites

- Python 3.8+
- pip or conda

## 🛠️ Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/grid-analytics-dashboard.git
cd grid-analytics-dashboard
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Streamlit Secrets (Local Development)
Create `.streamlit/secrets.toml`:
```bash
mkdir -p .streamlit
cp secrets_template.toml .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml`:
```toml
API_BASE_URL = "http://localhost:5000"
```

## 🏃 Running Locally

### Terminal 1: Start the Mock API
```bash
python api.py
```
You should see:
```
🚀 Starting Grid Analytics Mock API...
📡 API running on http://localhost:5000
```

### Terminal 2: Start the Streamlit Dashboard
```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📊 API Endpoints

The Flask mock API provides the following endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/nodes` | GET | Grid node metadata |
| `/api/lmp` | GET | LMP with components (Energy, Congestion, Loss) |
| `/api/congestion` | GET | Active transmission constraints |
| `/api/storage` | GET | Energy storage status |
| `/api/historical` | GET | 24-hour historical LMP data |
| `/api/price-spread` | GET | Day-Ahead vs Real-Time spreads |
| `/api/ancillary-services` | GET | Ancillary service prices |
| `/api/renewable-generation` | GET | Wind and solar generation |
| `/api/demand-forecast` | GET | 24-hour load forecast |

## 🎯 Dashboard Pages

1. **Dashboard Overview**: Key metrics and summary
2. **LMP Analysis**: Detailed component breakdown with filtering
3. **Congestion Monitoring**: Transmission constraint tracking with alerts
4. **Energy Storage**: Battery charge/discharge and SOC monitoring
5. **Historical Trends**: 24-hour price history and statistics
6. **Price Spread Analysis**: DA-RT spread visualization
7. **Settings**: Configuration and documentation

## 🔌 Integrating Real ERCOT API

When you obtain ERCOT API credentials:

1. **Update `.streamlit/secrets.toml`**:
```toml
ERCOT_SUBSCRIPTION_KEY = "your_key_here"
ERCOT_ID_TOKEN = "your_token_here"
```

2. **Create ERCOT API Connector** (`ercot_connector.py`):
```python
import requests

def fetch_ercot_lmp():
    subscription_key = st.secrets["ERCOT_SUBSCRIPTION_KEY"]
    id_token = st.secrets["ERCOT_ID_TOKEN"]
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Authorization": f"Bearer {id_token}"
    }
    # Fetch from ERCOT endpoint
    response = requests.get("https://api.ercot.com/...", headers=headers)
    return response.json()
```

3. **Update `app.py`** to use real data source

## 📁 Project Structure

```
grid-analytics-dashboard/
├── app.py                 # Streamlit dashboard application
├── api.py                 # Flask mock API server
├── requirements.txt       # Python dependencies
├── secrets_template.toml  # Streamlit secrets template
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── README.md             # This file
├── .gitignore
└── docs/
    └── API_DOCUMENTATION.md
```

## 🚀 Deployment

### Deploy on Streamlit Cloud

1. Push code to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Click "New app" and connect your GitHub repo
4. Set secrets in Streamlit Cloud settings:
   - `API_BASE_URL`: Your deployed API URL
   - `ERCOT_SUBSCRIPTION_KEY`: Your ERCOT key (if using real API)
   - `ERCOT_ID_TOKEN`: Your ERCOT token (if using real API)

### Deploy API on Heroku/AWS/GCP

The Flask API can be deployed on:
- **Heroku**: `git push heroku main`
- **AWS EC2/Lightsail**: Run as background service
- **Google Cloud Run**: Containerized deployment
- **DigitalOcean**: App Platform

## 📝 Configuration

### Streamlit Config (`.streamlit/config.toml`)

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[client]
showErrorDetails = true

[logger]
level = "info"
```

## 🔐 Security Best Practices

1. **Never commit secrets** to version control
2. Use `.gitignore` to exclude `.streamlit/secrets.toml`
3. Use environment variables for sensitive data
4. Validate all API inputs
5. Rate limit API endpoints in production
6. Use HTTPS for all communications
7. Rotate ERCOT API keys regularly

## 📖 API Documentation

Detailed API documentation is available in `docs/API_DOCUMENTATION.md`

## 🧪 Testing

### Test API Endpoints
```bash
# Health check
curl http://localhost:5000/api/health

# Get LMP data
curl http://localhost:5000/api/lmp

# Get storage data
curl http://localhost:5000/api/storage
```

### Test Streamlit App
- Navigate through all pages
- Verify data updates every 5 minutes (cache TTL)
- Test filters and interactions
- Check mobile responsiveness

## 🐛 Troubleshooting

### API Connection Error
```
Failed to connect to API: Connection refused
```
**Solution**: Ensure Flask API is running on port 5000

### Streamlit Cache Not Updating
```
Data appears stale
```
**Solution**: Cache TTL is 5 minutes by default. Use Ctrl+F to force refresh.

### Module Import Error
```
ModuleNotFoundError: No module named 'flask'
```
**Solution**: Reinstall dependencies: `pip install -r requirements.txt`

## 📚 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [LMP Basics](https://en.wikipedia.org/wiki/Locational_marginal_pricing)
- [ERCOT Public API Guide](https://developer.ercot.com/)
- [Electricity Grid Basics](https://www.energy.gov/)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Support & Contact

For questions or issues:
- Open an issue on GitHub
- Contact: your.email@example.com

## 🗺️ Roadmap

- [ ] Real ERCOT API integration
- [ ] Machine learning price forecasting
- [ ] Mobile app
- [ ] Database persistence
- [ ] User authentication
- [ ] Advanced OPF calculations
- [ ] Shift factor analysis
- [ ] Constraint relaxation analysis
- [ ] Multi-ISO support (CAISO, PJM, etc.)
- [ ] Alert system with notifications

## 🎉 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Flask](https://flask.palletsprojects.com/)
- Visualizations by [Plotly](https://plotly.com/)
- Data from ERCOT (when integrated)

---

**Ready to Deploy?**
1. Update the repository URL in the clone command
2. Push to GitHub
3. Deploy on Streamlit Cloud
4. Enjoy real-time grid analytics! ⚡
