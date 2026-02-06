import streamlit as st
import math

# ---------- Page Config ----------
st.set_page_config(page_title="Smart Hospital Dispatch", layout="centered")

st.title("🚨 Smart Accident Detection & Rescue System")
st.write("Automatic hospital selection based on distance and ICU bed availability")

# ---------- Distance Function ----------
def calculate_dist(lat1, lon1, lat2, lon2):
    radius = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    return round(radius * 2 * math.asin(math.sqrt(a)), 2)

# ---------- Hospital Dispatch UI ----------
def render_hospital_data(accident):
    st.subheader("🏥 Smart Hospital Dispatch")

    if not accident:
        st.info("No accident detected. Hospitals are on standby.")
        return

    acc_lat, acc_lon = 11.0168, 76.9558  # Accident Location (Gandhipuram)

    hospitals = [
        {"name": "CMCH", "lat": 11.0001, "lon": 76.9600, "beds": 0},
        {"name": "PSG Hospitals", "lat": 11.0250, "lon": 76.9950, "beds": 8},
        {"name": "KMCH", "lat": 11.0450, "lon": 77.0350, "beds": 15},
    ]

    available = []

    for h in hospitals:
        dist = calculate_dist(acc_lat, acc_lon, h["lat"], h["lon"])

        if h["beds"] > 0:
            available.append((dist, h))

        if h["beds"] > 0:
            st.success(f"🚑 {h['name']} → {dist} km | {h['beds']} ICU Beds")
        else:
            st.warning(f"❌ {h['name']} → {dist} km | NO ICU Beds")

    if available:
        best = min(available, key=lambda x: x[0])
        st.markdown("---")
        st.success(
            f"✅ **Auto Selected Hospital:** {best[1]['name']} "
            f"({best[0]} km | {best[1]['beds']} ICU Beds)"
        )
    else:
        st.error("⚠️ No hospitals currently have ICU beds available!")

# ---------- MAIN UI ----------
accident = st.toggle("🚨 Accident Detected")

render_hospital_data(accident)
