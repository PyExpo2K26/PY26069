import streamlit as st

def setup_page():
    st.set_page_config(
        page_title="G-Trace Emergency System",
        page_icon="🚨",
        layout="wide"
    )

def render_header(accident):
    st.title("🚨 G-Trace Smart Rescue System")
    if accident:
        st.error("Emergency Protocol Activated")
    else:
        st.success("System Monitoring Active")

# run UI
setup_page()
render_header(False)
