import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta
import json

# Set page config
st.set_page_config(page_title="Grid Analytics Dashboard", layout="wide")

# Title and Description
st.title("⚡ Grid Analytics & LMP Dashboard")
st.markdown("""
This dashboard provides real-time and historical analysis of grid data, including:
- **LMP Components**: Energy, Congestion, and Loss pricing
- **Grid Congestion**: Transmission constraint monitoring
- **Energy Storage**: Battery charging/discharging status
- **Historical Analysis**: Time-series price trends
- **Price Spreads**: Day-ahead vs Real-time comparison
""")

# API Configuration
API_BASE_URL = st.secrets.get("API_BASE_URL", "http://localhost:5000")

# Helper function to fetch data from mock API
@st.cache_data(ttl=300)
def fetch_api_data(endpoint):
    """Fetch data from mock API with caching"""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Failed to connect to API: {e}")
        return None

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select View", [
    "Dashboard Overview",
    "LMP Analysis",
    "Congestion Monitoring",
    "Energy Storage",
    "Historical Trends",
    "Price Spread Analysis",
    "Settings"
])

# ==================== DASHBOARD OVERVIEW ====================
if page == "Dashboard Overview":
    st.header("Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Fetch data
    nodes_data = fetch_api_data("/api/nodes")
    lmp_data = fetch_api_data("/api/lmp")
    storage_data = fetch_api_data("/api/storage")
    
    if lmp_data and nodes_data:
        lmp_df = pd.DataFrame(lmp_data)
        
        with col1:
            avg_lmp = lmp_df['total_lmp'].mean()
            st.metric("Avg LMP", f"${avg_lmp:.2f}/MWh")
        
        with col2:
            max_lmp = lmp_df['total_lmp'].max()
            st.metric("Max LMP", f"${max_lmp:.2f}/MWh")
        
        with col3:
            avg_congestion = lmp_df['congestion'].mean()
            st.metric("Avg Congestion", f"${avg_congestion:.2f}/MWh")
        
        with col4:
            if storage_data:
                storage_df = pd.DataFrame(storage_data)
                total_discharge = storage_df['discharge_mw'].sum()
                st.metric("Total Storage Discharge", f"{total_discharge:.2f} MW")
    
    st.divider()
    
    # LMP by Node
    if lmp_data:
        st.subheader("LMP by Node")
        lmp_df = pd.DataFrame(lmp_data)
        
        fig = px.bar(lmp_df, x='node', y='total_lmp', 
                     title="Total LMP by Node",
                     color='congestion',
                     color_continuous_scale='RdYlGn_r',
                     labels={'total_lmp': 'LMP ($/MWh)', 'node': 'Grid Node'})
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(lmp_df, use_container_width=True)

# ==================== LMP ANALYSIS ====================
elif page == "LMP Analysis":
    st.header("LMP Analysis")
    
    # Component filter
    col1, col2 = st.columns([1, 3])
    with col1:
        component_filter = st.selectbox(
            "Select Component",
            ["Total LMP", "Energy Component", "Congestion Component", "Loss Component"]
        )
    
    lmp_data = fetch_api_data("/api/lmp")
    
    if lmp_data:
        lmp_df = pd.DataFrame(lmp_data)
        
        # Determine column to plot
        if component_filter == "Energy Component":
            y_col = "energy"
        elif component_filter == "Congestion Component":
            y_col = "congestion"
        elif component_filter == "Loss Component":
            y_col = "loss"
        else:
            y_col = "total_lmp"
        
        # Stacked bar chart for all components
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Energy', x=lmp_df['node'], y=lmp_df['energy']))
        fig.add_trace(go.Bar(name='Congestion', x=lmp_df['node'], y=lmp_df['congestion']))
        fig.add_trace(go.Bar(name='Loss', x=lmp_df['node'], y=lmp_df['loss']))
        
        fig.update_layout(barmode='stack', title='LMP Components by Node',
                         xaxis_title='Grid Node', yaxis_title='Price ($/MWh)',
                         hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
        
        # Component detail table
        st.subheader("Detailed LMP Components")
        st.dataframe(lmp_df, use_container_width=True)
        
        # Statistics
        st.subheader("Component Statistics")
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        
        with stats_col1:
            st.metric("Avg Energy Price", f"${lmp_df['energy'].mean():.2f}")
        with stats_col2:
            st.metric("Avg Congestion", f"${lmp_df['congestion'].mean():.2f}")
        with stats_col3:
            st.metric("Avg Loss Component", f"${lmp_df['loss'].mean():.2f}")

# ==================== CONGESTION MONITORING ====================
elif page == "Congestion Monitoring":
    st.header("Congestion Monitoring")
    
    congestion_data = fetch_api_data("/api/congestion")
    lmp_data = fetch_api_data("/api/lmp")
    
    if lmp_data:
        lmp_df = pd.DataFrame(lmp_data)
        
        # Congestion severity chart
        fig = px.bar(lmp_df.sort_values('congestion', ascending=False),
                    x='node', y='congestion',
                    title='Congestion Component by Node',
                    color='congestion',
                    color_continuous_scale='Reds',
                    labels={'congestion': 'Congestion ($/MWh)', 'node': 'Grid Node'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Alert threshold
        threshold = st.slider("Congestion Alert Threshold ($/MWh)", 0, 20, 10)
        
        high_congestion = lmp_df[lmp_df['congestion'] > threshold]
        if not high_congestion.empty:
            st.warning(f"⚠️ {len(high_congestion)} node(s) exceeding congestion threshold")
            st.dataframe(high_congestion, use_container_width=True)
        else:
            st.success("✅ All nodes below congestion threshold")
    
    # Congestion events
    if congestion_data:
        st.subheader("Active Congestion Events")
        events_df = pd.DataFrame(congestion_data)
        st.dataframe(events_df, use_container_width=True)

# ==================== ENERGY STORAGE ====================
elif page == "Energy Storage":
    st.header("Energy Storage Monitoring")
    
    storage_data = fetch_api_data("/api/storage")
    
    if storage_data:
        storage_df = pd.DataFrame(storage_data)
        
        # Storage status by node
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Charge (MW)', x=storage_df['node'], y=storage_df['charge_mw'], marker_color='green'))
        fig.add_trace(go.Bar(name='Discharge (MW)', x=storage_df['node'], y=storage_df['discharge_mw'], marker_color='red'))
        
        fig.update_layout(barmode='group', title='Battery Charge/Discharge by Node',
                         xaxis_title='Grid Node', yaxis_title='Power (MW)',
                         hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
        
        # Storage summary
        st.subheader("Storage Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Charge Capacity", f"{storage_df['charge_mw'].sum():.2f} MW")
        with col2:
            st.metric("Total Discharge Capacity", f"{storage_df['discharge_mw'].sum():.2f} MW")
        with col3:
            st.metric("Net Output", f"{storage_df['net_output_mw'].sum():.2f} MW")
        with col4:
            st.metric("Avg Net per Node", f"{storage_df['net_output_mw'].mean():.2f} MW")
        
        st.dataframe(storage_df, use_container_width=True)

# ==================== HISTORICAL TRENDS ====================
elif page == "Historical Trends":
    st.header("Historical Price Trends")
    
    historical_data = fetch_api_data("/api/historical")
    
    if historical_data:
        hist_df = pd.DataFrame(historical_data)
        hist_df['timestamp'] = pd.to_datetime(hist_df['timestamp'])
        
        fig = px.line(hist_df, x='timestamp', y='lmp',
                     title='24-Hour LMP History (Node A)',
                     labels={'lmp': 'LMP ($/MWh)', 'timestamp': 'Time'},
                     markers=True)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Historical Data")
        st.dataframe(hist_df, use_container_width=True)
        
        # Statistics
        st.subheader("Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Min LMP", f"${hist_df['lmp'].min():.2f}")
        with col2:
            st.metric("Max LMP", f"${hist_df['lmp'].max():.2f}")
        with col3:
            st.metric("Avg LMP", f"${hist_df['lmp'].mean():.2f}")
        with col4:
            st.metric("Std Dev", f"${hist_df['lmp'].std():.2f}")

# ==================== PRICE SPREAD ANALYSIS ====================
elif page == "Price Spread Analysis":
    st.header("Day-Ahead vs Real-Time Price Spread")
    
    spread_data = fetch_api_data("/api/price-spread")
    
    if spread_data:
        spread_df = pd.DataFrame(spread_data)
        spread_df['timestamp'] = pd.to_datetime(spread_df['timestamp'])
        
        fig = px.bar(spread_df, x='timestamp', y='da_rt_spread',
                    title='DA-RT Price Spread Over 24 Hours',
                    color='da_rt_spread',
                    color_continuous_scale='RdBu',
                    labels={'da_rt_spread': 'Spread ($/MWh)', 'timestamp': 'Time'})
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Spread Analysis")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            positive = len(spread_df[spread_df['da_rt_spread'] > 0])
            st.metric("DA > RT (Hours)", positive)
        with col2:
            negative = len(spread_df[spread_df['da_rt_spread'] < 0])
            st.metric("RT > DA (Hours)", negative)
        with col3:
            avg_spread = spread_df['da_rt_spread'].mean()
            st.metric("Avg Spread", f"${avg_spread:.2f}")
        
        st.dataframe(spread_df, use_container_width=True)

# ==================== SETTINGS ====================
elif page == "Settings":
    st.header("Settings")
    
    st.subheader("API Configuration")
    st.info(f"**Current API Base URL:** {API_BASE_URL}")
    
    st.write("""
    ### Configuration Guide
    
    To connect to your mock API:
    1. Ensure your Flask API is running on `http://localhost:5000`
    2. Or set `API_BASE_URL` in your Streamlit secrets file (`.streamlit/secrets.toml`)
    
    Example `.streamlit/secrets.toml`:
    ```
    API_BASE_URL = "http://localhost:5000"
    ERCOT_SUBSCRIPTION_KEY = "your_key_here"
    ERCOT_ID_TOKEN = "your_token_here"
    ```
    
    ### Mock API Endpoints
    - `/api/nodes` — Grid node metadata
    - `/api/lmp` — LMP with components
    - `/api/congestion` — Congestion events
    - `/api/storage` — Storage resource data
    - `/api/historical` — 24-hour historical prices
    - `/api/price-spread` — DA-RT price spreads
    """)
    
    st.subheader("About This Dashboard")
    st.write("""
    This dashboard is built with:
    - **Streamlit**: Web framework
    - **Plotly**: Interactive visualizations
    - **Pandas**: Data processing
    - **Flask Mock API**: Data source
    
    Ready to integrate with real ERCOT API when credentials are available.
    """)
