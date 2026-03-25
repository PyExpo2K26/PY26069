
import streamlit as st
import pandas as pd

def render_map(accident):
    st.subheader("📍 Emergency Path Tracking")
    if accident:
        # Shows Accident (Gandhipuram) and Hospital (PSG)
        map_data = pd.DataFrame({
            "lat": [11.0168, 11.0250], 
            "lon": [76.9558, 76.9950]
        })
        st.map(map_data, zoom=12)
        st.caption("🔴 Accident Point | 🔵 Assigned Hospital Location")
    else:
        st.info("✅ No active incidents detected on GPS.")
render_map(True)
