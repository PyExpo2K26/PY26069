import streamlit as st
import ui_layout
import ui_sidebar
import ui_alerts
import ui_map_placeholder
import ui_hospitals

# 1. Setup the Page (Wide layout, G-Trace Icon)
ui_layout.setup_page()

# 2. Render Header
ui_layout.render_header(False)

# 3. Render Sidebar Simulation Controls
# This takes the sliders from your ui_alerts file
speed, impact, accident_detected = ui_alerts.render_controls()

# 4. Render the Map (Coimbatore location)
ui_map_placeholder.render_map(accident_detected)

# 5. Show Emergency Alerts and Hospitals if accident is detected
if accident_detected:
    ui_sidebar.render_alerts(True)
    ui_hospitals.render_hospital_data(True)
else:
    st.info("System Monitoring: No issues detected.")