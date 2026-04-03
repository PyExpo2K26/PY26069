 🚨 G-Trace — Because Every Second Counts

> *Every year, thousands of road accident victims lose their lives not because help wasn't available — but because help arrived too late.*
> **G-Trace was built to fix that.**

 What is G-Trace?

G-Trace is a smart, IoT-powered accident detection and emergency response system. The moment a vehicle is involved in a serious crash, G-Trace **automatically detects it, pinpoints the location, finds the nearest hospital, and places an emergency call** — all within seconds, and all without any human intervention.

No waiting. No panic dialing. No delays.

Think of it as having a silent co-pilot that never sleeps — one that springs into action the instant something goes wrong.

---

## 🎬 Demo

📽️ **[Watch the Demo Video](https://drive.google.com/file/d/1hiDPNkK7vUIAMd7pv7JGhw-qiDEHBweL/view?usp=sharing)




 The Problem We're Solving

India alone sees **over 4.5 lakh road accidents every year**. A significant portion of deaths are preventable — if only the victim had reached a hospital within the first 60 minutes, what doctors call the **"Golden Hour."**

The current process looks like this:
- Someone witnesses the crash (or doesn't)
- They dial emergency services (if they have signal)
- They try to describe the location (which they may not know)
- Help is dispatched (finally)

That chain can take **20-40 minutes** just to get started.

G-Trace compresses that entire chain into **under 10 seconds.**

---

 How It Works

The system runs in three clean stages:

```
🔴  DETECT         →        📍  LOCATE        →        🚑  DISPATCH
Accelerometer            GPS coordinates            Nearest hospital
reads G-force            locked instantly           found + call made
> 10G = accident         via Neo-6M module          via Twilio API
```

 Stage 1 — Detection
An **ADXL345 accelerometer** mounted in the vehicle continuously measures motion in all three axes (X, Y, Z). The resultant G-force is calculated in real-time. When it exceeds the accident threshold (10G), the system kicks in immediately.

 Stage 2 — Localization
A **Neo-6M GPS module** provides real-time latitude and longitude of the accident site. If GPS hasn't locked yet, the system still proceeds with the last known coordinates — no single point of failure.

Stage 3 — Emergency Response
The **Flask backend** queries OpenStreetMap's live database to find the nearest hospital within the area. Then, using **Twilio**, it places an automated voice call to emergency contacts with the exact location, impact severity, hospital name, and a Google Maps link — all spoken out loud.


 🛠️ Tech Stack

|  Hardware | ESP32, ADXL345 Accelerometer, Neo-6M GPS |
|  Firmware | Arduino C++ (I2C, WiFi, HTTP) |
|  Backend | Python, Flask, Twilio, OpenStreetMap Overpass API |
|  Dashboard | Streamlit, Pandas |
|  Mapping | OpenStreetMap (live hospital search, Haversine distance) |
|  Alerts | Twilio Programmable Voice (automated emergency call) |

---

## 📁 Repository Structure

```
PY26069/
│
├── code/                        # All source code
│   ├── app.py                   # Streamlit dashboard (frontend)
│   ├── backend.py               # Flask REST API (backend)
│   ├── hardware.py              # ESP32 Arduino firmware
│   ├── ui_alerts.py             # Alert UI module
│   ├── ui_hospitals.py          # Hospital display module
│   ├── ui_layout.py             # Dashboard layout
│   ├── ui_map_placeholder.py    # Map module
│   ├── ui_sidebar.py            # Sidebar controls
│   ├── ui_traffic.py            # Traffic status module
│   └── requirements.txt        # Python dependencies
│
└── documentation/               # All project documents
    ├── README.md                # This file
    ├── demo-video/              # Demo video / link
    ├── sop/                     # Standard Operating Procedure
    ├── research/                # Research papers & references
    └── other-docs/              # Additional documentation
```

---

## 🚀 Running It Yourself

 Prerequisites
- Python 3.7 or higher
- A Twilio account (free trial works)
- ESP32 + ADXL345 + Neo-6M (for hardware mode)

 1. Clone the repo
```bash
git clone https://github.com/PyExpo2K26/PY26069.git
cd PY26069/code
```

 2. Install dependencies
```bash
pip install -r requirements.txt
```

 3. Set up environment variables
Create a `.env` file inside the `code/` folder:
```
TWILION_ACC_SID=your_twilio_account_sid
TWILION_AUTH_TOKEN=your_twilio_auth_token
TWILION_PHONE_NUMBER=your_twilio_phone_number
```

 4. Start the backend
```bash
python backend.py
```
Backend runs at `http://localhost:5000`

5. Start the dashboard
```bash
streamlit run app.py
```
Dashboard opens in your browser automatically.

 6. Test without hardware
Open the dashboard → use the **"Test G-Force" slider** → drag it to **10.0 or above** → watch the system respond in real time.

 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API info and available routes |
| POST | `/data` | Receive sensor data from ESP32 |
| GET | `/status` | Current system state (JSON) |
| POST | `/reset` | Reset accident state |
| POST | `/test-accident` | Trigger a mock accident |
| GET | `/logs` | Recent activity logs |
| GET | `/health` | Health check |
| GET | `/hardware` | Hardware connection status |



✨ Features
Sub-10-second response** from impact to emergency call
Live hospital search** using real OpenStreetMap data — not hardcoded
Automated voice call** with GPS coordinates, impact severity, and maps link
Real-time dashboard** showing accident site, hospital, ETA, and rescue timeline
Software-only test mode** — simulate accidents without any hardware
Auto-expanding search** — if no hospital found in 5km, expands to 15km
Persistent state** — accident data saved even if server restarts

 What's Next

We're not done. Here's what's coming:

- 🟢 **Green Corridor** — automatically clear traffic signals along the ambulance route
- 📱 **SMS alerts** to family members with live tracking link
- 🧠 **False positive filtering** — distinguish a pothole from a real crash using ML
- 🔌 **Live hardware integration** — fully tested with physical ESP32 + sensors
