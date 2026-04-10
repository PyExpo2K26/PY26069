from flask import Flask, request, jsonify
import math
import json
import os
from datetime import datetime
from twilio.rest import Client

app = Flask(__name__)

# ===== TWILIO CONFIG =====
TWILIO_SID   = os.environ.get("TWILIO_SID",   "AC5825ad806cb9819b8ec4b6d7cc2e2913")
TWILIO_TOKEN = os.environ.get("TWILIO_TOKEN", "b257ee9c6c686205b7842a03b45cb200")
TWILIO_FROM  = os.environ.get("TWILIO_FROM",  "+17543184157")
CALL_TO      = os.environ.get("CALL_TO",      "+917010467865")   # India number with country code

# ===== DEFAULT COIMBATORE LOCATION (used when GPS is invalid) =====
DEFAULT_LAT = 11.0168
DEFAULT_LON = 76.9558

# ===== ACCIDENT THRESHOLD (must match ESP32 gForceThreshold = 1.0) =====
ACCIDENT_G_THRESHOLD = 1.0

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
    "call_made"           : False,
    "connected"           : False,
    "hardware_id"         : None,
    "logs"                : []
}

DATA_FILE = "accident_status.json"


# ─────────────────────────────────────────
# TWILIO EMERGENCY CALL
# ─────────────────────────────────────────
def make_emergency_call(lat, lon, g_force, hospital_name, distance_km):
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)

        twiml_message = f"""
        <Response>
            <Say voice="alice" loop="3">
                Emergency Alert from G Trace System.
                Vehicle accident detected.
                Impact severity {round(g_force, 1)} G force.
                Accident location coordinates,
                latitude {lat}, longitude {lon}.
                Nearest hospital is {hospital_name},
                approximately {distance_km} kilometers away.
                Google Maps link:
                https://maps.google.com/?q={lat},{lon}
                Please dispatch ambulance immediately.
            </Say>
        </Response>
        """

        call = client.calls.create(
            twiml=twiml_message,
            to=CALL_TO,
            from_=TWILIO_FROM
        )

        print(f"✅ Emergency call made! SID: {call.sid}")
        return True

    except Exception as e:
        print(f"❌ Twilio call error: {e}")
        return False


# ─────────────────────────────────────────
# HAVERSINE DISTANCE
# ─────────────────────────────────────────
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ─────────────────────────────────────────
# COIMBATORE HOSPITALS (manual data)
# ─────────────────────────────────────────
HOSPITALS = [
    {"name": "Ganga Hospital",                          "lat": 11.0168, "lon": 76.9558},
    {"name": "PSG Hospitals",                           "lat": 11.0245, "lon": 76.9516},
    {"name": "KMCH (Kovai Medical Center and Hospital)","lat": 11.0122, "lon": 76.9614},
    {"name": "Sri Ramakrishna Hospital",                "lat": 11.0200, "lon": 76.9580},
    {"name": "Coimbatore Medical College Hospital",     "lat": 11.0018, "lon": 76.9614},
    {"name": "Gem Hospital",                            "lat": 11.0200, "lon": 76.9500},
    {"name": "Aravind Eye Hospital",                    "lat": 11.0210, "lon": 76.9630},
    {"name": "G. Kuppuswamy Naidu Memorial Hospital",   "lat": 11.0076, "lon": 76.9674},
]

def get_nearest_hospital(lat, lon):
    hospitals = []
    for h in HOSPITALS:
        d = haversine(lat, lon, h["lat"], h["lon"])
        hospitals.append({**h, "dist": d})
    hospitals.sort(key=lambda h: h["dist"])
    nearest = hospitals[0]
    all_names = [f"{h['name']} ({round(h['dist'], 1)} km)" for h in hospitals]
    return nearest["name"], round(nearest["dist"], 2), nearest["lat"], nearest["lon"], all_names


# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
def save_state():
    with open(DATA_FILE, "w") as f:
        json.dump(state, f, indent=2)

def load_state():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                loaded = json.load(f)
                state.update(loaded)
        except Exception as e:
            print(f"⚠ Could not load saved state: {e}")

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{timestamp} | {message}"
    print(entry)
    state["logs"].append(entry)
    if len(state["logs"]) > 100:
        state["logs"] = state["logs"][-100:]
    save_state()


# ─────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────

@app.route("/data", methods=["POST"])
def receive_data():
    try:
        data = request.get_json(force=True)
        if not data or "g_force" not in data:
            return jsonify({"error": "'g_force' is required"}), 400

        g_force   = float(data["g_force"])
        gps_valid = bool(data.get("gps_valid", False))

        # Use real GPS if valid, else fallback to Coimbatore city center
        if gps_valid:
            p_lat = float(data.get("lat", DEFAULT_LAT))
            p_lon = float(data.get("lon", DEFAULT_LON))
        else:
            p_lat = DEFAULT_LAT
            p_lon = DEFAULT_LON
            log("⚠ GPS invalid — using Coimbatore default coordinates")

        state["g_force"]     = round(g_force, 3)
        state["lat"]         = p_lat
        state["lon"]         = p_lon
        state["gps_valid"]   = gps_valid
        state["connected"]   = True
        state["hardware_id"] = data.get("hardware_id", "ESP32")

        log(f"📡 Data received | Device={state['hardware_id']} | G={g_force:.3f} | GPS={'valid' if gps_valid else 'invalid'} | Pos=({p_lat:.5f},{p_lon:.5f})")

        # ── Accident check — matches ESP32 threshold of 1.0g ──
        accident_flag     = bool(data.get("accident", False))
        accident_detected = g_force > ACCIDENT_G_THRESHOLD or accident_flag

        if accident_detected:
            state["accident_detected"] = True
            state["timestamp"]         = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            state["call_made"]         = False

            log(f"🚨 ACCIDENT CONFIRMED | G={g_force:.3f} | Pos=({p_lat},{p_lon})")
            log("🔍 Finding nearest hospital...")

            name, dist, h_lat, h_lon, all_names = get_nearest_hospital(p_lat, p_lon)

            state["nearest_hospital"]     = name
            state["nearest_hospital_lat"] = h_lat
            state["nearest_hospital_lon"] = h_lon
            state["distance_km"]          = dist
            state["all_hospitals"]        = all_names

            log(f"🏥 Nearest: {name} ({dist} km away)")
            log(f"📞 Placing emergency call to {CALL_TO}...")

            call_success       = make_emergency_call(p_lat, p_lon, g_force, name, dist)
            state["call_made"] = call_success

            if call_success:
                log("✅ Emergency call placed successfully")
            else:
                log("❌ Emergency call FAILED — check Twilio credentials")

            save_state()

            return jsonify({
                "accident"     : True,
                "hospital"     : name,
                "distance_km"  : dist,
                "hospital_lat" : h_lat,
                "hospital_lon" : h_lon,
                "all_hospitals": all_names,
                "location"     : [p_lat, p_lon],
                "call_made"    : call_success
            }), 200

        # Normal (non-accident) data
        save_state()
        return jsonify({"accident": False, "g_force": g_force}), 200

    except Exception as e:
        print(f"❌ Error in /data: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/status", methods=["GET"])
def get_status():
    return jsonify(state), 200


@app.route("/logs", methods=["GET"])
def get_logs():
    return jsonify({"logs": state["logs"]}), 200


@app.route("/test-accident", methods=["POST"])
def test_accident():
    """Manually fire a test accident (uses Coimbatore default location)."""
    lat, lon  = DEFAULT_LAT, DEFAULT_LON
    g_force   = 2.5

    state["accident_detected"] = True
    state["g_force"]           = g_force
    state["lat"]               = lat
    state["lon"]               = lon
    state["gps_valid"]         = False
    state["timestamp"]         = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state["connected"]         = True

    log(f"🧪 TEST ACCIDENT triggered | G={g_force} | Pos=({lat},{lon})")

    name, dist, h_lat, h_lon, all_names = get_nearest_hospital(lat, lon)

    state["nearest_hospital"]     = name
    state["nearest_hospital_lat"] = h_lat
    state["nearest_hospital_lon"] = h_lon
    state["distance_km"]          = dist
    state["all_hospitals"]        = all_names

    log(f"🏥 Nearest: {name} ({dist} km)")
    log(f"📞 Placing test emergency call...")

    call_success       = make_emergency_call(lat, lon, g_force, name, dist)
    state["call_made"] = call_success

    save_state()

    return jsonify({
        "message"     : "Test accident triggered",
        "accident"    : True,
        "hospital"    : name,
        "distance_km" : dist,
        "call_made"   : call_success
    }), 200


@app.route("/reset", methods=["POST"])
def reset_system():
    state.update({
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
        "call_made"           : False,
        "connected"           : False,
        "hardware_id"         : None
    })
    save_state()
    log("🔄 System reset by user")
    return jsonify({"message": "System reset successful"}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status"          : "ok",
        "json_file_exists": os.path.exists(DATA_FILE),
        "accident_active" : state["accident_detected"],
        "call_made"       : state["call_made"],
        "threshold_g"     : ACCIDENT_G_THRESHOLD
    }), 200


if __name__ == "__main__":
    load_state()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🚀  G-Trace Flask Backend")
    print(f"   Accident threshold : {ACCIDENT_G_THRESHOLD} g")
    print(f"   Default location   : Coimbatore ({DEFAULT_LAT}, {DEFAULT_LON})")
    print(f"   Emergency call to  : {CALL_TO}")
    print(f"   Listening          : http://10.121.96.135:5000")
    print(f"   Data file          : {os.path.abspath(DATA_FILE)}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    # use_reloader=False prevents watchdog from restarting on unrelated file changes
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
