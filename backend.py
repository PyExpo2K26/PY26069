from flask import Flask, request, jsonify
import math
import requests
import json
import os
from datetime import datetime, timedelta
from twilio.rest import Client
from dotenv import load_dotenv
import os
load_dotenv()  

app = Flask(__name__)

TWILIO_SID   = os.getenv("TWILION_ACC_SID")
TWILIO_TOKEN = os.getenv("TWILION_AUTH_TOKEN")
TWILIO_FROM  = os.getenv("TWILION_PHONE_NUMBER")  
CALL_TO      = "+918220387221"  

# Logs storage
logs_list = []
MAX_LOGS = 100

def log_output(message):
    """Custom logging function to capture output."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    logs_list.append(log_entry)
    if len(logs_list) > MAX_LOGS:
        logs_list.pop(0)
    print(message)  


state = {
    "accident_detected"   : False,
    "g_force"             : 0.0,
    "lat"                 : None,
    "lon"                 : None,
    "gps_valid"           : False,
    "nearest_hospital"    : "None",
    "nearest_hospital_lat": None,
    "nearest_hospital_lon": None,
    "distance_km"         : 0.0,
    "all_hospitals"       : [],
    "timestamp"           : None,
"call_made"       : False,
    "hardware_id"     : None,
    "last_ping"       : None,
    "connected"       : False
}

DATA_FILE = "accident_status.json"


def make_emergency_call(lat, lon, g_force, hospital_name, distance_km):
    if not TWILIO_SID or not TWILIO_TOKEN:
        log_output(f"MOCK EMERGENCY CALL (creds missing): {hospital_name}, {distance_km}km")
        return True

    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)

        twiml_message = f"""
        <Response>
            <Say voice="alice" loop="2">
                Emergency Alert from G Trace System.
                Vehicle accident detected.
                Impact severity {g_force} G force.
                Accident location coordinates,
                {lat} latitude, {lon} longitude.
                Nearest hospital is {hospital_name},
                approximately {distance_km} kilometers away.
                Google Maps link,
                https://maps.google.com/?q={lat},{lon}
                Please dispatch ambulance immediately.
            </Say>
        </Response>
        """

        call = client.calls.create(
            twiml  = twiml_message,
            to     = CALL_TO,
            from_  = TWILIO_FROM
        )

        log_output(f"REAL Emergency call made! SID: {call.sid}")
        return True

    except Exception as e:
        log_output(f"Twilio call error: {e}")
        return False


def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def osm_find_hospitals(lat, lon, radius_meters=5000):
    log_output(f"OSM query: {radius_meters}m around ({lat},{lon})")
    overpass_query = f"""
    [out:json][timeout:25];
    (
      node["amenity"="hospital"](around:{radius_meters},{lat},{lon});
      way["amenity"="hospital"](around:{radius_meters},{lat},{lon});
      node["amenity"="clinic"](around:{radius_meters},{lat},{lon});
      node["amenity"="doctors"](around:{radius_meters},{lat},{lon});
    );
    out center;
    """
    try:
        response = requests.post(
            "https://overpass-api.de/api/interpreter",
            data={"data": overpass_query},
            headers={"User-Agent": "GTrace-Emergency/1.0"},
            timeout=20
        )
        response.raise_for_status()
        elements = response.json().get("elements", [])

        hospitals = []
        for el in elements:
            h_lat = el.get("lat") or el.get("center", {}).get("lat")
            h_lon = el.get("lon") or el.get("center", {}).get("lon")
            name  = el.get("tags", {}).get("name", "Unnamed Hospital")

            if h_lat and h_lon and name != "Unnamed Hospital":
                dist = haversine(lat, lon, float(h_lat), float(h_lon))
                hospitals.append({
                    "name": name,
                    "lat" : float(h_lat),
                    "lon" : float(h_lon),
                    "dist": dist
                })

        if not hospitals:
            if radius_meters < 15000:
                log_output(f"No hospitals within {radius_meters}m, expanding...")
                return osm_find_hospitals(lat, lon, radius_meters + 5000)
            log_output("No hospitals found within 15km")
            return None

        hospitals.sort(key=lambda h: h["dist"])
        nearest   = hospitals[0]
        all_names = [f"{h['name']} ({round(h['dist'], 1)} km)" for h in hospitals]

        log_output(f"OSM: {len(hospitals)} hospitals found")
        log_output(f"   Nearest: {nearest['name']} ({round(nearest['dist'], 2)} km)")

        return nearest["name"], round(nearest["dist"], 2), nearest["lat"], nearest["lon"], all_names

    except requests.exceptions.Timeout:
        log_output("Overpass API timed out")
        return None
    except Exception as e:
        log_output(f"OSM error: {e}")
        return None


def save_state():
    with open(DATA_FILE, "w") as f:
        json.dump(state, f, indent=2)


@app.route("/data", methods=["POST"])
def receive_data():
    try:
        data = request.get_json(force=True)
        if not data or "g_force" not in data:
            return jsonify({"error": "'g_force' is required"}), 400

        g_force   = float(data["g_force"])
        p_lat     = float(data.get("lat", 11.0830))
        p_lon     = float(data.get("lon", 77.0210))
        gps_valid = bool(data.get("gps_valid", False))

        state["g_force"]   = round(g_force, 3)
        state["lat"]       = p_lat
        state["lon"]       = p_lon
        state["gps_valid"] = gps_valid

        log_output(f"Received: G={g_force:.2f} | GPS={'valid' if gps_valid else 'estimated'} ({p_lat:.5f}, {p_lon:.5f})")
        
        state["hardware_id"] = data.get("hardware_id", "unknown")
        state["last_ping"] = datetime.now().isoformat()
        state["connected"] = True

        accident_override = data.get("accident", False)

        if g_force > 10.0 or accident_override:
            state["accident_detected"] = True
            state["timestamp"]         = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            state["call_made"]         = False

            log_output(f"ACCIDENT CONFIRMED at ({p_lat}, {p_lon}) {'(TEST MODE)' if accident_override else ''}")
            log_output("Querying OSM for nearest hospital...")

            result = osm_find_hospitals(p_lat, p_lon)

            if result:
                name, dist, h_lat, h_lon, all_names = result
                state["nearest_hospital"]       = name
                state["nearest_hospital_lat"]   = h_lat
                state["nearest_hospital_lon"]   = h_lon
                state["distance_km"]            = dist
                state["all_hospitals"]          = all_names

                log_output("Calling emergency contact...")
                log_output("Accident detected and alerting through call...")
                call_success = make_emergency_call(
                    p_lat, p_lon,
                    round(g_force, 2) if not accident_override else 12.5,
                    name, dist
                )
                state["call_made"] = call_success

                location_message = f"Location {p_lat}, {p_lon} has been shared" if gps_valid and not (p_lat == 0.0 and p_lon == 0.0) else "No GPS module found"

            else:
                state["nearest_hospital"]     = "OSM Unavailable — Call 108"
                state["nearest_hospital_lat"] = None
                state["nearest_hospital_lon"] = None
                state["distance_km"]          = 0.0
                state["all_hospitals"]        = []

                log_output("Calling emergency contact (no hospital found)...")
                log_output("Accident detected and alerting through call...")
                call_success = make_emergency_call(
                    p_lat, p_lon,
                    round(g_force, 2) if not accident_override else 12.5,
                    "unknown, please check maps", 0
                )
                state["call_made"] = call_success

                location_message = f"Location {p_lat}, {p_lon} has been shared" if gps_valid and not (p_lat == 0.0 and p_lon == 0.0) else "No GPS module found"

            save_state()

            return jsonify({
                "accident"     : True,
                "hospital"     : state["nearest_hospital"],
                "distance_km"  : state["distance_km"],
                "hospital_lat" : state["nearest_hospital_lat"],
                "hospital_lon" : state["nearest_hospital_lon"],
                "all_hospitals": state["all_hospitals"],
                "location"     : [p_lat, p_lon],
                "call_made"    : state["call_made"],
                "message"      : location_message
            }), 200

        save_state()
        return jsonify({"accident": False, "g_force": g_force}), 200

    except Exception as e:
        log_output(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/status", methods=["GET"])
def check_status():
    # Update connected status
    if state["last_ping"]:
        last_ping_dt = datetime.fromisoformat(state["last_ping"])
        state["connected"] = (datetime.now() - last_ping_dt) < timedelta(minutes=5)
    
    save_state()
    return jsonify(state), 200

@app.route("/reset", methods=["POST"])
def reset_system():
    state.update({
        "accident_detected"   : False,
        "g_force"             : 0.0,
        "nearest_hospital"    : "None",
        "nearest_hospital_lat": None,
        "nearest_hospital_lon": None,
        "distance_km"         : 0.0,
        "all_hospitals"       : [],
        "timestamp"           : None,
        "call_made"           : False
    })
    save_state()
    log_output("System reset.")
    return jsonify({"message": "System reset successful"}), 200

@app.route("/hardware", methods=["GET"])
def hardware_status():
    if not state["last_ping"]:
        return jsonify({"connected": False, "hardware_id": state["hardware_id"], "last_ping": None}), 200
    
    last_ping_dt = datetime.fromisoformat(state["last_ping"])
    is_connected = (datetime.now() - last_ping_dt) < timedelta(minutes=5)
    state["connected"] = is_connected  # Update
    
    return jsonify({
        "connected": is_connected,
        "hardware_id": state["hardware_id"],
        "last_ping": state["last_ping"],
        "uptime_min": round((datetime.now() - last_ping_dt).total_seconds() / 60, 1)
    })

@app.route("/test-accident", methods=["POST"])
def test_accident():
    try:
        data = request.get_json(force=True) or {}
        test_lat = float(data.get("lat", 11.0830))
        test_lon = float(data.get("lon", 77.0210))
        
        state["accident_detected"] = True
        state["g_force"] = 12.5
        state["lat"] = test_lat
        state["lon"] = test_lon
        state["gps_valid"] = True
        state["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_output(f"MOCK ACCIDENT test at ({test_lat}, {test_lon})")
        
        result = osm_find_hospitals(test_lat, test_lon)
        if result:
            name, dist, h_lat, h_lon, all_names = result
            state["nearest_hospital"] = name
            state["nearest_hospital_lat"] = h_lat
            state["nearest_hospital_lon"] = h_lon
            state["distance_km"] = dist
            state["all_hospitals"] = all_names
            call_success = make_emergency_call(test_lat, test_lon, 12.5, name, dist)
        else:
            # Fallback test hospital
            state["nearest_hospital"] = "KMCH Hospital (Fallback)"
            state["nearest_hospital_lat"] = 11.0500
            state["nearest_hospital_lon"] = 77.0400
            state["distance_km"] = 4.2
            state["all_hospitals"] = ["KMCH (4.2km)", "PSG (5.1km)"]
            call_success = make_emergency_call(test_lat, test_lon, 12.5, "KMCH (test)", 4.2)
        
        state["call_made"] = call_success
        save_state()
        
        return jsonify({"message": "Mock accident triggered", "accident": True, **state}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status"          : "ok",
        "json_file_exists": os.path.exists(DATA_FILE),
        "accident_active" : state["accident_detected"],
        "call_made"       : state["call_made"]
    }), 200

@app.route("/logs", methods=["GET"])
def get_logs():
    """Return recent logs for frontend display."""
    return jsonify({"logs": logs_list}), 200


@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "message": "G-Trace Backend Active",
        "endpoints": {
            "/": "GET - This page",
            "/status": "GET - Current accident state (JSON)",
            "/health": "GET - Health check",
            "/data": "POST - Send sensor data {'g_force', 'lat', 'lon', 'gps_valid'}",
            "/reset": "POST - Reset system state"
        },
        "data_file": DATA_FILE,
        "docs": "POST to /data with g_force>10 to simulate accident"
    })

if __name__ == "__main__":
    startup_msg = [
        "=" * 50,
        "G-Trace Flask Server",
        "OSM Hospital Search + Twilio Auto Call",
        f"Listening  -> http://10.121.234.29:5000",
        f"Data file  -> {os.path.abspath(DATA_FILE)}",
        "=" * 50
    ]
    
    for msg in startup_msg:
        print(msg)
        log_output(msg)
    
    app.run(host="0.0.0.0", port=5000, debug=True)