import streamlit as st

def setup_page():
    # Only called by main.py
    pass

def render_header(accident):
    if accident:
        st.markdown("<h1 style='color:red;'>🚨 G-TRACE: EMERGENCY DISPATCH ACTIVE</h1>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='color:green;'>📡 G-TRACE: SYSTEM MONITORING</h1>", unsafe_allow_html=True)  

setup_page()
render_header(False)