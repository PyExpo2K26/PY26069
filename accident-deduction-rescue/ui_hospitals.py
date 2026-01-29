import streamlit as st

st.set_page_config(page_title="Hospital Dispatch", layout="centered")

st.title("🚨 Smart Accident Detection & Rescue System")

def render_hospital_data(accident):

    st.subheader("🏥 Emergency Hospital Dispatch")

    if not accident:
        st.info("Hospitals on standby.")
        return

    hospitals = [
        {"name": "CMCH", "distance": 2.3},
        {"name": "PSG Hospitals", "distance": 3.1},
        {"name": "Kovai Medical Center", "distance": 4.5}
    ]

    nearest = min(hospitals, key=lambda x: x["distance"])

    for h in hospitals:
        if h == nearest:
            st.success(f"🚑 Ambulance dispatched: {h['name']} ({h['distance']} km)")
        else:
            st.write(f"{h['name']} - {h['distance']} km")

st.subheader("⚠ Accident Status")

accident_detected = st.checkbox("Accident Detected")

render_hospital_data(accident_detected)
