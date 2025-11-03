from flask import Flask, jsonify
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# ==================== EXPANDED STATIC DATA ====================
# Grid nodes with locations (ERCOT region, Texas) - EXPANDED
NODES = [
    # Load Centers (High Congestion)
    {"node": "A", "name": "North Dallas", "lat": 32.85, "lon": -96.68, "type": "Load Center", "demand_mw": 4500},
    {"node": "B", "name": "Houston Downtown", "lat": 29.76, "lon": -95.37, "type": "Load Center", "demand_mw": 5200},
    {"node": "C", "name": "San Antonio", "lat": 29.42, "lon": -98.49, "type": "Load Center", "demand_mw": 3100},
    {"node": "D", "name": "Austin", "lat": 30.27, "lon": -97.74, "type": "Load Center", "demand_mw": 2800},
    {"node": "E", "name": "Fort Worth", "lat": 32.76, "lon": -97.33, "type": "Load Center", "demand_mw": 2400},
    
    # Generation Centers (Low Congestion)
    {"node": "F", "name": "West Texas Wind", "lat": 31.94, "lon": -101.87, "type": "Generation", "demand_mw": -1200},
    {"node": "G", "name": "Coastal Generation", "lat": 28.24, "lon": -97.04, "type": "Generation", "demand_mw": -1800},
    {"node": "H", "name": "Panhandle Solar", "lat": 34.41, "lon": -100.55, "type": "Generation", "demand_mw": -900},
    {"node": "I", "name": "Central Plant", "lat": 31.55, "lon": -97.15, "type": "Generation", "demand_mw": -2100},
    {"node": "J", "name": "Northeast Reserve", "lat": 33.20, "lon": -95.50, "type": "Generation", "demand_mw": -1400},
]

# Battery/Storage Locations
STORAGE_NODES = {
    "A": {"capacity_mwh": 250, "efficiency": 0.88, "name": "Dallas Battery Complex"},
    "B": {"capacity_mwh": 400, "efficiency": 0.89, "name": "Houston Energy Storage"},
    "C": {"capacity_mwh": 180, "efficiency": 0.87, "name": "San Antonio Battery Park"},
    "D": {"capacity_mwh": 220, "efficiency": 0.88, "name": "Austin Storage Hub"},
    "G": {"capacity_mwh": 350, "efficiency": 0.89, "name": "Coastal Storage Facility"},
}

# ==================== ROUTES ====================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat(), "api_version": "2.0"})

@app.route('/api/nodes', methods=['GET'])
def get_nodes():
    """Returns grid node metadata"""
    return jsonify(NODES)

@app.route('/api/lmp', methods=['GET'])
def get_lmp():
    """Returns LMP data with components (Energy, Congestion, Loss) - ENHANCED"""
    lmp_data = []
    
    # Get current hour for realistic pricing
    current_hour = datetime.now().hour
    
    # Base energy price varies by hour (peak: 7-9am, 5-9pm)
    if current_hour in [7, 8, 17, 18, 19, 20]:
        base_energy = np.random.uniform(55, 85)  # Peak hours
    elif current_hour in [22, 23, 0, 1, 2, 3, 4, 5]:
        base_energy = np.random.uniform(25, 40)  # Off-peak/night
    else:
        base_energy = np.random.uniform(40, 60)  # Mid-peak
    
    for n in NODES:
        # Energy component: influenced by time of day and node type
        energy = base_energy + np.random.uniform(-5, 5)
        
        # Congestion: much higher at load centers, near zero at generation
        if n["type"] == "Load Center":
            congestion = np.random.uniform(8, 35)  # Higher spread for testing
        else:
            congestion = np.random.uniform(-5, 2)  # Can be negative at generation
        
        # Loss component: varies by distance and demand
        loss = abs(n["demand_mw"]) / 500 + np.random.uniform(0.5, 2)
        
        total_lmp = energy + congestion + loss
        
        lmp_data.append({
            "node": n["node"],
            "node_name": n["name"],
            "energy": round(max(0, energy), 2),
            "congestion": round(congestion, 2),
            "loss": round(loss, 2),
            "total_lmp": round(max(0, total_lmp), 2),
            "node_type": n["type"],
            "timestamp": datetime.now().isoformat()
        })
    
    return jsonify(lmp_data)

@app.route('/api/congestion', methods=['GET'])
def get_congestion():
    """Returns active congestion constraints and events - EXPANDED"""
    constraints = [
        {
            "constraint_id": "TC_001",
            "name": "Dallas North 345kV Line",
            "node": "A",
            "severity": "High",
            "flow_percent": round(np.random.uniform(92, 108), 1),
            "limit_mw": 450,
            "current_mw": round(np.random.uniform(410, 480), 1),
            "duration_hours": np.random.randint(1, 8),
            "reason": "Peak demand + Outage on backup line"
        },
        {
            "constraint_id": "TC_002",
            "name": "Houston Load Relief Transformer",
            "node": "B",
            "severity": "High",
            "flow_percent": round(np.random.uniform(88, 102), 1),
            "limit_mw": 550,
            "current_mw": round(np.random.uniform(480, 560), 1),
            "duration_hours": np.random.randint(1, 6),
            "reason": "Summer peak demand"
        },
        {
            "constraint_id": "TC_003",
            "name": "San Antonio Interconnect",
            "node": "C",
            "severity": "Medium",
            "flow_percent": round(np.random.uniform(70, 85), 1),
            "limit_mw": 350,
            "current_mw": round(np.random.uniform(245, 297), 1),
            "duration_hours": np.random.randint(2, 5),
            "reason": "Normal operation"
        },
        {
            "constraint_id": "TC_004",
            "name": "Austin Central Corridor",
            "node": "D",
            "severity": "Low",
            "flow_percent": round(np.random.uniform(55, 70), 1),
            "limit_mw": 320,
            "current_mw": round(np.random.uniform(176, 224), 1),
            "duration_hours": np.random.randint(1, 4),
            "reason": "Light load"
        },
        {
            "constraint_id": "TC_005",
            "name": "Coastal Wind Integration Line",
            "node": "G",
            "severity": "Medium",
            "flow_percent": round(np.random.uniform(75, 90), 1),
            "limit_mw": 1200,
            "current_mw": round(np.random.uniform(900, 1080), 1),
            "duration_hours": np.random.randint(2, 7),
            "reason": "High wind generation"
        },
        {
            "constraint_id": "TC_006",
            "name": "West Texas Export Line",
            "node": "F",
            "severity": "Low",
            "flow_percent": round(np.random.uniform(40, 60), 1),
            "limit_mw": 800,
            "current_mw": round(np.random.uniform(320, 480), 1),
            "duration_hours": np.random.randint(0, 3),
            "reason": "Wind variability"
        }
    ]
    return jsonify(constraints)

@app.route('/api/storage', methods=['GET'])
def get_storage():
    """Returns energy storage resource status and output - EXPANDED"""
    storage_data = []
    current_hour = datetime.now().hour
    
    for node_id, storage_info in STORAGE_NODES.items():
        # Smart charging: charge during low price (night), discharge during peak
        if current_hour in [7, 8, 17, 18, 19, 20]:  # Peak hours - discharge
            discharge = np.random.uniform(80, min(200, storage_info["capacity_mwh"]/2))
            charge = np.random.uniform(0, 10)
            soc = np.random.uniform(20, 50)
        elif current_hour in [22, 23, 0, 1, 2, 3, 4, 5]:  # Night - charge
            charge = np.random.uniform(60, min(150, storage_info["capacity_mwh"]/2))
            discharge = np.random.uniform(0, 10)
            soc = np.random.uniform(30, 70)
        else:  # Mid-peak - light discharge
            discharge = np.random.uniform(20, 60)
            charge = np.random.uniform(10, 40)
            soc = np.random.uniform(40, 80)
        
        net_output = discharge - charge
        
        storage_data.append({
            "node": node_id,
            "node_name": storage_info["name"],
            "capacity_mwh": storage_info["capacity_mwh"],
            "charge_mw": round(charge, 2),
            "discharge_mw": round(discharge, 2),
            "net_output_mw": round(net_output, 2),
            "soc_percent": round(soc, 1),
            "efficiency_percent": round(storage_info["efficiency"] * 100, 1),
            "power_loss_mw": round((charge + discharge) * (1 - storage_info["efficiency"]), 2),
            "timestamp": datetime.now().isoformat()
        })
    
    return jsonify(storage_data)

@app.route('/api/historical', methods=['GET'])
def get_historical():
    """Returns 24-hour historical LMP data for Node A - ENHANCED"""
    try:
        historical_data = []
        
        for i in range(24):
            # Calculate time going backwards
            time_offset = timedelta(hours=(23-i))
            timestamp = datetime.now() - time_offset
            hour = timestamp.hour
            
            # Base price with realistic daily seasonality
            if 6 <= hour < 9:  # Morning peak ramp
                base_price = np.random.uniform(50, 75)
            elif 9 <= hour < 17:  # Daytime (lower)
                base_price = np.random.uniform(35, 55)
            elif 17 <= hour < 21:  # Evening peak
                base_price = np.random.uniform(60, 95)
            elif 21 <= hour < 22:  # Evening decline
                base_price = np.random.uniform(45, 65)
            else:  # Night/early morning (lowest)
                base_price = np.random.uniform(20, 40)
            
            # Add some volatility
            volatility = np.random.uniform(-8, 8)
            lmp = base_price + volatility
            
            historical_data.append({
                "timestamp": timestamp.isoformat(),
                "node": "A",
                "node_name": "North Dallas",
                "lmp": round(max(0, lmp), 2),
                "energy": round(max(0, lmp * 0.70), 2),
                "congestion": round(lmp * 0.20, 2),
                "loss": round(max(0, lmp * 0.10), 2),
                "demand_mw": round(np.random.uniform(3500, 5500), 0),
                "renewable_percent": round(np.random.uniform(10, 40), 1)
            })
        
        return jsonify(historical_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/price-spread', methods=['GET'])
def get_price_spread():
    """Returns Day-Ahead to Real-Time price spread over 24 hours - ENHANCED"""
    try:
        spread_data = []
        
        for i in range(24):
            time_offset = timedelta(hours=(23-i))
            timestamp = datetime.now() - time_offset
            hour = timestamp.hour
            
            # DA prices (forecasted 24 hours ago)
            if hour in [7, 8, 17, 18, 19, 20]:
                da_price = np.random.uniform(60, 90)
            else:
                da_price = np.random.uniform(30, 50)
            
            # RT prices can deviate significantly from DA
            # Often lower in off-peak, higher in unpredicted peaks
            deviation = np.random.uniform(-12, 15)  # Wide spread for realism
            rt_price = da_price + deviation
            rt_price = max(0, rt_price)  # Can't be negative
            
            spread = da_price - rt_price
            
            spread_data.append({
                "timestamp": timestamp.isoformat(),
                "node": "A",
                "node_name": "North Dallas",
                "day_ahead_price": round(da_price, 2),
                "real_time_price": round(rt_price, 2),
                "da_rt_spread": round(spread, 2),
                "spread_direction": "DA Premium" if spread > 1 else ("RT Premium" if spread < -1 else "Neutral"),
                "spread_magnitude": round(abs(spread), 2),
                "wind_forecast_error": round(np.random.uniform(-5, 5), 1),  # %
                "solar_forecast_error": round(np.random.uniform(-8, 8), 1)   # %
            })
        
        return jsonify(spread_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ancillary-services', methods=['GET'])
def get_ancillary_services():
    """Returns ancillary service prices and battery participation - ENHANCED"""
    services = [
        {
            "service": "Regulation Up",
            "price": round(np.random.uniform(20, 50), 2),
            "battery_participation_mw": round(np.random.uniform(40, 120), 2),
            "traditional_gen_mw": round(np.random.uniform(80, 200), 2),
            "total_mw": round(np.random.uniform(150, 280), 2),
            "battery_percent": round(np.random.uniform(25, 45), 1)
        },
        {
            "service": "Regulation Down",
            "price": round(np.random.uniform(10, 35), 2),
            "battery_participation_mw": round(np.random.uniform(30, 100), 2),
            "traditional_gen_mw": round(np.random.uniform(60, 180), 2),
            "total_mw": round(np.random.uniform(100, 250), 2),
            "battery_percent": round(np.random.uniform(20, 40), 1)
        },
        {
            "service": "Responsive Reserves",
            "price": round(np.random.uniform(8, 20), 2),
            "battery_participation_mw": round(np.random.uniform(60, 150), 2),
            "traditional_gen_mw": round(np.random.uniform(150, 300), 2),
            "total_mw": round(np.random.uniform(250, 400), 2),
            "battery_percent": round(np.random.uniform(30, 50), 1)
        },
        {
            "service": "ERCOT Contingency Reserve",
            "price": round(np.random.uniform(15, 40), 2),
            "battery_participation_mw": round(np.random.uniform(80, 180), 2),
            "traditional_gen_mw": round(np.random.uniform(200, 400), 2),
            "total_mw": round(np.random.uniform(350, 550), 2),
            "battery_percent": round(np.random.uniform(20, 35), 1)
        }
    ]
    return jsonify(services)

@app.route('/api/renewable-generation', methods=['GET'])
def get_renewable_generation():
    """Returns renewable generation status - ENHANCED"""
    current_hour = datetime.now().hour
    
    # Wind is better at night
    if 20 <= current_hour or current_hour < 8:
        wind_output = np.random.uniform(3000, 5500)
    elif 12 <= current_hour < 16:
        wind_output = np.random.uniform(1000, 3000)
    else:
        wind_output = np.random.uniform(2000, 4000)
    
    # Solar peaks at noon
    if 8 <= current_hour < 17:
        solar_output = max(0, 2500 * np.sin((current_hour - 8) * np.pi / 9) + np.random.uniform(-200, 200))
    else:
        solar_output = np.random.uniform(0, 100)
    
    renewable_data = {
        "timestamp": datetime.now().isoformat(),
        "wind_mw": round(wind_output, 2),
        "wind_capacity_mw": 9000,
        "wind_percent_capacity": round((wind_output / 9000) * 100, 1),
        "solar_mw": round(solar_output, 2),
        "solar_capacity_mw": 3500,
        "solar_percent_capacity": round((solar_output / 3500) * 100, 1),
        "renewable_total_mw": round(wind_output + solar_output, 2),
        "renewable_capacity_mw": 12500,
        "renewable_percent_of_capacity": round(((wind_output + solar_output) / 12500) * 100, 1),
        "renewable_percent_of_load": round(((wind_output + solar_output) / 20000) * 100, 1),  # Assuming 20GW load
        "forecast_next_hour_mw": round(wind_output * np.random.uniform(0.8, 1.2), 2)
    }
    return jsonify(renewable_data)

@app.route('/api/demand-forecast', methods=['GET'])
def get_demand_forecast():
    """Returns load forecast for next 24 hours - ENHANCED"""
    try:
        forecast_data = []
        current_demand = np.random.uniform(18000, 22000)
        
        for i in range(24):
            timestamp = datetime.now() + timedelta(hours=i)
            hour = timestamp.hour
            
            # Realistic hourly load pattern
            if 6 <= hour < 9:  # Morning peak ramp
                base_load = 21000 + np.random.uniform(-500, 500)
            elif 9 <= hour < 16:  # Daytime (moderate)
                base_load = 19000 + np.random.uniform(-500, 500)
            elif 16 <= hour < 21:  # Evening peak
                base_load = 22000 + np.random.uniform(-500, 500)
            elif 21 <= hour < 23:  # Evening decline
                base_load = 20000 + np.random.uniform(-500, 500)
            else:  # Night/early morning
                base_load = 17000 + np.random.uniform(-500, 500)
            
            # Add confidence decreasing over time
            confidence = max(85, 98 - (i * 0.5))
            
            forecast_data.append({
                "timestamp": timestamp.isoformat(),
                "forecast_load_mw": round(base_load, 2),
                "confidence_percent": round(confidence, 1),
                "uncertainty_mw": round(base_load * 0.05, 2),  # ±5% uncertainty
                "lower_bound_mw": round(base_load * 0.95, 2),
                "upper_bound_mw": round(base_load * 1.05, 2),
                "prev_day_actual_mw": round(base_load * np.random.uniform(0.95, 1.05), 2)
            })
        
        return jsonify(forecast_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== ERROR HANDLING ====================
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error", "details": str(error)}), 500

# ==================== MAIN ====================
if __name__ == '__main__':
    print("🚀 Starting Grid Analytics Mock API (ENHANCED)...")
    print("📡 API running on http://localhost:5000")
    print("📊 Enhanced Features:")
    print("   ✅ 10 Grid Nodes (5 load centers + 5 generation centers)")
    print("   ✅ 5 Storage/Battery Locations")
    print("   ✅ 6 Active Congestion Events")
    print("   ✅ Realistic Hourly Patterns (Peak/Off-peak)")
    print("   ✅ Wind/Solar Generation Curves")
    print("   ✅ Smart Battery Charging (Peak/Off-peak)")
    print("   ✅ DA-RT Price Spreads with Volatility")
    print("   ✅ 4 Ancillary Services with Battery Participation")
    print("   ✅ Demand Forecast with Confidence Intervals")
    print("\n📊 Available endpoints:")
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
