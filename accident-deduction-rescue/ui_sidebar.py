import streamlit as st

st.set_page_config(page_title="G-Trace Emergency Dashboard", layout="centered")

st.title("🚨 G-Trace Emergency Dashboard")

def render_alerts(accident):
    st.subheader("🔔 Emergency Response Log")
    if accident:
        st.error("⚠️ CRITICAL ALERT: Impact detected at Gandhipuram")
        st.info("🚑 DISPATCHED: Ambulance ID AMB-CB-09")
        st.warning("🚦 Traffic Priority Override: ACTIVE")
    else:
        st.success("✅ System Monitoring: All Emergency Units Standby")

# ---- Simulation Control ----
st.subheader("🎮 Simulation Control")
accident = st.toggle("Simulate Accident")

#
render_alerts(accident)
