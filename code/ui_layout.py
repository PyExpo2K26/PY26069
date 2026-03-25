import streamlit as st
import pandas as pd
import random
from datetime import datetime


# -------------------- UI FUNCTION -------------------- #
def render_ui():

    # Page Config
    st.set_page_config(
        page_title="G-Trace Emergency System",
        page_icon="🚨",
        layout="wide"
    )

    # Sidebar
    st.sidebar.header("Control Panel")
    accident = st.sidebar.toggle("Simulate Accident", value=False)
    st.sidebar.caption("G-Trace v2.1")

    # Header
    st.title("🚨 G-Trace Smart Rescue System")

    if accident:
        st.error("Emergency Detected • Rescue Protocol Activated")
    else:
        st.success("System Monitoring Active")

    st.caption(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("---")

    # Dashboard Metrics
    col1, col2, col3 = st.columns(3)

    col1.metric("Vehicle Speed", f"{random.randint(50,100)} km/h")
    col2.metric("Impact Sensor", "High Impact" if accident else "Normal")
    col3.metric("Rescue Status", "Dispatching 🚑" if accident else "Standby")

    st.markdown("---")

    # Emergency Section
    if accident:
        st.subheader("Emergency Response Workflow")
        st.write("• Impact detected")
        st.write("• Location transmitted")
        st.write("• Contacts notified")
        st.write("• Ambulance dispatched")

        # Map
        data = pd.DataFrame({
            "lat": [28.6139 + random.uniform(-0.01, 0.01)],
            "lon": [77.2090 + random.uniform(-0.01, 0.01)]
        })
        st.map(data)

    else:
        st.info("All systems operating normally.")


# -------------------- RUN APP -------------------- #
if __name__ == "__main__":
    render_ui()
