from flask import Flask, jsonify
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# ==================== STATIC DATA ====================
# Grid nodes with locations (ERCOT region, Texas)
NODES = [
    {"node": "A", "name": "North Dallas", "lat": 32.85, "lon": -96.68, "type": "Load Center"},
    {"node": "B", "name": "Houston", "lat": 29.76, "lon": -95.37, "type": "Load Center"},
    {"node": "C", "name": "San Antonio", "lat": 29.42, "lon": -98.49, "type": "Load Center"},
    {"node": "D", "name": "West Texas", "lat": 31.94, "lon": -101.87, "type": "Generation"},
    {"node": "E", "name": "Coastal", "lat": 28.24, "lon": -97.04, "type": "Generation"}
]

# ==================== ROUTES ====================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/nodes', methods=['GET'])
def get_nodes():
    """Returns grid node metadata"""
    return jsonify(NODES)

@app.route('/api/lmp', methods=['GET'])
def get_lmp():
    """Returns LMP data with components (Energy, Congestion, Loss)"""
    lmp_data = []
    
    for n in NODES:
        # Simulate realistic LMP values
        # Energy component: base price influenced by load (varies 30-55)
        energy = np.random.uniform(30, 55)
        
        # Congestion component: higher at load centers, lower at generation points
        if n["type"] == "Load Center":
            congestion = np.random.uniform(5, 20)
        else:
            congestion = np.random.uniform(0, 5)
        
        # Loss component: represents transmission losses (1-3 $/MWh)
        loss = np.random.uniform(1, 3)
        
        total_lmp = energy + congestion + loss
        
        lmp_data.append({
            "node": n["node"],
            "node_name": n["name"],
            "energy": round(energy, 2),
            "congestion": round(congestion, 2),
            "loss": round(loss, 2),
            "total_lmp": round(total_lmp, 2),
            "timestamp": datetime.now().isoformat()
        })
    
    return jsonify(lmp_data)

@app.route('/api/congestion', methods=['GET'])
def get_congestion():
    """Returns active congestion constraints and events"""
    constraints = [
        {
            "constraint_id": "TC_001",
            "name": "Dallas North 345kV Line",
            "node": "A",
            "severity": "High" if np.random.random() > 0.6 else "Medium",
            "flow_percent": round(np.random.uniform(85, 105), 1),
            "limit_mw": 450,
            "current_mw": round(np.random.uniform(380, 470), 1),
            "duration_hours": np.random.randint(1, 8)
        },
        {
            "constraint_id": "TC_002",
            "name": "Houston Load Relief Transformer",
            "node": "B",
            "severity": "Medium" if np.random.random() > 0.5 else "Low",
            "flow_percent": round(np.random.uniform(70, 95), 1),
            "limit_mw": 350,
            "current_mw": round(np.random.uniform(240, 340), 1),
            "duration_hours": np.random.randint(1, 6)
        },
        {
            "constraint_id": "TC_003",
            "name": "San Antonio Interconnect",
            "node": "C",
            "severity": "Low",
            "flow_percent": round(np.random.uniform(45, 75), 1),
            "limit_mw": 280,
            "current_mw": round(np.random.uniform(125, 210), 1),
            "duration_hours": np.random.randint(0, 4)
        }
    ]
    return jsonify(constraints)

@app.route('/api/storage', methods=['GET'])
def get_storage():
    """Returns energy storage resource status and output"""
    storage_data = []
    
    for n in NODES:
        # Simulate battery cycling
        charge = np.random.uniform(0, 50)
        discharge = np.random.uniform(0, 50)
        
        # Avoid simultaneous charge and discharge
        if charge > 25:
            discharge = np.random.uniform(0, 10)
        
        net_output = discharge - charge
        
        storage_data.append({
            "node": n["node"],
            "node_name": n["name"],
            "capacity_mwh": np.random.uniform(100, 500),
            "charge_mw": round(charge, 2),
            "discharge_mw": round(discharge, 2),
            "net_output_mw": round(net_output, 2),
            "soc_percent": round(np.random.uniform(20, 95), 1),  # State of Charge
            "efficiency_percent": 88.0,
            "timestamp": datetime.now().isoformat()
        })
    
    return jsonify(storage_data)

@app.route('/api/historical', methods=['GET'])
def get_historical():
    """Returns 24-hour historical LMP data for Node A"""
    base_time = datetime.now().normalize()
    hours = pd.date_range(base_time - timedelta(hours=24), periods=24, freq='H')
    
    # Generate realistic price curve (lower at night, higher during peak)
    historical_data = []
    for i, t in enumerate(hours):
        hour = t.hour
        
        # Base price with daily seasonality
        if 6 <= hour < 9:  # Morning peak
            base_price = np.random.uniform(45, 60)
        elif 17 <= hour < 21:  # Evening peak
            base_price = np.random.uniform(48, 65)
        elif 0 <= hour < 6:  # Night (low)
            base_price = np.random.uniform(25, 35)
        else:  # Off-peak
            base_price = np.random.uniform(35, 45)
        
        historical_data.append({
            "timestamp": t.isoformat(),
            "node": "A",
            "node_name": "North Dallas",
            "lmp": round(base_price, 2),
            "energy": round(base_price * 0.75, 2),
            "congestion": round(base_price * 0.15, 2),
            "loss": round(base_price * 0.10, 2)
        })
    
    return jsonify(historical_data)

@app.route('/api/price-spread', methods=['GET'])
def get_price_spread():
    """Returns Day-Ahead to Real-Time price spread over 24 hours"""
    base_time = datetime.now().normalize()
    hours = pd.date_range(base_time - timedelta(hours=24), periods=24, freq='H')
    
    spread_data = []
    for t in hours:
        # DA prices typically trend 3-8 hours ahead, RT can deviate based on real conditions
        da_price = np.random.uniform(35, 55)
        rt_price = da_price + np.random.uniform(-5, 8)  # RT can be higher or lower
        spread = da_price - rt_price
        
        spread_data.append({
            "timestamp": t.isoformat(),
            "node": "A",
            "node_name": "North Dallas",
            "day_ahead_price": round(da_price, 2),
            "real_time_price": round(rt_price, 2),
            "da_rt_spread": round(spread, 2),
            "spread_direction": "DA Premium" if spread > 0 else "RT Premium"
        })
    
    return jsonify(spread_data)

@app.route('/api/ancillary-services', methods=['GET'])
def get_ancillary_services():
    """Returns ancillary service prices and battery participation"""
    services = [
        {
            "service": "Regulation Up",
            "price": round(np.random.uniform(15, 35), 2),
            "battery_participation_mw": round(np.random.uniform(20, 80), 2),
            "traditional_gen_mw": round(np.random.uniform(50, 150), 2)
        },
        {
            "service": "Regulation Down",
            "price": round(np.random.uniform(8, 20), 2),
            "battery_participation_mw": round(np.random.uniform(15, 60), 2),
            "traditional_gen_mw": round(np.random.uniform(40, 120), 2)
        },
        {
            "service": "Responsive Reserves",
            "price": round(np.random.uniform(5, 12), 2),
            "battery_participation_mw": round(np.random.uniform(30, 100), 2),
            "traditional_gen_mw": round(np.random.uniform(100, 200), 2)
        }
    ]
    return jsonify(services)

@app.route('/api/renewable-generation', methods=['GET'])
def get_renewable_generation():
    """Returns renewable generation status"""
    renewable_data = {
        "timestamp": datetime.now().isoformat(),
        "wind_mw": round(np.random.uniform(1000, 5000), 2),
        "wind_capacity_mw": 8000,
        "solar_mw": round(np.random.uniform(200, 2000), 2),
        "solar_capacity_mw": 2500,
        "renewable_total_mw": round(np.random.uniform(1500, 6500), 2),
        "renewable_percent_of_load": round(np.random.uniform(15, 45), 1)
    }
    return jsonify(renewable_data)

@app.route('/api/demand-forecast', methods=['GET'])
def get_demand_forecast():
    """Returns load forecast for next 24 hours"""
    base_time = datetime.now().normalize()
    hours = pd.date_range(base_time, periods=24, freq='H')
    
    forecast_data = []
    for t in hours:
        hour = t.hour
        
        # Base load pattern (lower at night, peak during day)
        if 6 <= hour < 9:
            base_load = np.random.uniform(35000, 38000)
        elif 17 <= hour < 21:
            base_load = np.random.uniform(40000, 45000)
        elif 0 <= hour < 6:
            base_load = np.random.uniform(25000, 30000)
        else:
            base_load = np.random.uniform(32000, 37000)
        
        forecast_data.append({
            "timestamp": t.isoformat(),
            "forecast_load_mw": round(base_load, 2),
            "confidence_percent": round(np.random.uniform(85, 98), 1)
        })
    
    return jsonify(forecast_data)

# ==================== ERROR HANDLING ====================
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

# ==================== MAIN ====================
if __name__ == '__main__':
    print("🚀 Starting Grid Analytics Mock API...")
    print("📡 API running on http://localhost:5000")
    print("📊 Available endpoints:")
    print("   - GET /api/health")
    print("   - GET /api/nodes")
    print("   - GET /api/lmp")
    print("   - GET /api/congestion")
    print("   - GET /api/storage")
    print("   - GET /api/historical")
    print("   - GET /api/price-spread")
    print("   - GET /api/ancillary-services")
    print("   - GET /api/renewable-generation")
    print("   - GET /api/demand-forecast")
    
    app.run(debug=True, port=5000, host='0.0.0.0')
