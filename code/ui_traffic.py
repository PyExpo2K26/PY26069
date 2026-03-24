import streamlit as st

st.set_page_config(page_title="Smart Traffic Control", layout="centered")

st.title("🚨 GPS-Based Accident Detection System")

def render_traffic_control(accident_detected):
    st.subheader("🚦 Smart Traffic Control (Green Corridor)")
    
    if accident_detected:
        st.success("🟢 Emergency Priority Mode: ACTIVE")
        st.info("Signals on Gandhipuram → Laxmi Mills → CMCH route set to Priority Green.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Gandhipuram Jnc", "GREEN", "Priority")
        with col2:
            st.metric("Laxmi Mills", "GREEN", "Priority")
        with col3:
            st.metric("CMCH Signal", "GREEN", "Priority")
    else:
        st.warning("🚥 Signals operating in standard automated mode.")
        st.write("No accident detected. Normal traffic flow maintained.")

# 🔘 User control (simulation)
accident_detected = st.checkbox("⚠️ Accident Detected")

# 🚦 Render traffic control system
render_traffic_control(accident_detected)
