import streamlit as st

def render_controls():
    st.sidebar.header("🎮 Simulation Controls")

    speed = st.sidebar.slider("Ambulance Speed", 1, 10, 5)
    impact = st.sidebar.slider("Impact Intensity", 1, 10, 5)

    accident_detected = impact >= 7

    if accident_detected:
        st.sidebar.error("🚨 Accident Detected!")
    else:
        st.sidebar.success("✅ Normal Driving")

    return speed, impact, accident_detected

# just 2 simple lines to run it
st.title("Accident Simulation")
render_controls()
