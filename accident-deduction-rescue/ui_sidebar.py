import streamlit as st

st.set_page_config(
    page_title="Accident Detection & Rescue",
    layout="centered"
)

st.title("🚨 Accident Detection & Rescue System")

st.sidebar.header("Control Panel")
accident_detected = st.sidebar.checkbox("Simulate Accident")

def render_alerts(accident):
    st.subheader("🔔 Emergency Alerts")

    if accident:
        st.error("⚠️ Accident detected!")
        st.warning("🚑 Ambulance dispatched")
        st.info("👮 Police notified")
    else:
        st.success("✅ No emergency alerts")

render_alerts(accident_detected)       


