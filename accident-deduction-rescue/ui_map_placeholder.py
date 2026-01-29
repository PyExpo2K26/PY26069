import streamlit as st
import pandas as pd

def render_map(accident):
    st.subheader("📍 GPS Accident Location")

    if accident:
        map_data = pd.DataFrame({
            "lat": [11.0168],
            "lon": [76.9558]
        })
        st.map(map_data, zoom=12)
        st.error("🚨 Accident at Gandhipuram, Coimbatore")
    else:
        st.info("✅ No accident detected")

# CALL THE FUNCTION
render_map(True)
