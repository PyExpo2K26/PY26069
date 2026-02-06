 G-Trace: Smart Accident Detection and Rescue System

G-Trace is an automated IoT-based emergency response platform. It uses a modular software design to detect vehicle accidents in real-time, locate the incident with GPS, and coordinate an immediate rescue response between hospitals and law enforcement. 

Project Overview

The main goal of G-Trace is to remove human delays in reporting road accidents. By automating detection and dispatch, the system ensures that medical help reaches the victim during the critical "Golden Hour."

The Three-Stage Logical Flow

Detection (The Sensor Layer): The system continuously monitors vehicle dynamics using a simulated tri-axial accelerometer.

Coordination (The Dispatch Layer): When an accident is detected, the system triggers a localized emergency state, locks GPS coordinates, and notifies authorities.

Rescue (The Action Layer): The system identifies the nearest hospital based on real-time distance calculations and dispatches an ambulance.

Key Technical Modules

The project uses a modular design, allowing each part of the rescue chain to work independently.

Accident Detection Logic (ui_alerts.py): Monitors "Impact Intensity," which reflects resultant G-force . An accident is classified at values $>6.0$.

GIS and Localization (ui_map_placeholder.py): Instantly retrieves and pins GPS coordinates, specifically for Gandhipuram, Coimbatore.

Smart Resource Allocation (ui_hospitals.py): Calculates distances to hospitals like CMCH (2.3 km) and PSG (3.1 km) for automated dispatch.

Command and Control (ui_sidebar.py and ui_layout.py): Manages the Emergency Response Center interface and notifications for multiple agencies.

How to Run the App

To run the G-Trace dashboard on your local machine, follow these steps:

1. Ensure Python is Installed: Make sure you have Python 3.7 or higher on your system.
2. Install Required Libraries: Open your terminal or VS Code terminal and install the necessary dependencies:
   ```
   pip install streamlit pandas
   ```
3. Download the Project Files: Make sure all modular files (ui_layout.py, ui_sidebar.py, ui_alerts.py, ui_map_placeholder.py, ui_hospitals.py) are in the same directory as your main execution script.
4. Execute the Application: Run the following command in your terminal:
   ```
   streamlit run your_main_script_name.py
   ```
   Replace your_main_script_name.py with the name of your file that contains the import streamlit and module integration code.

Mini Hack 1 Evaluation Scope (25%)

For this milestone, we successfully demonstrated:

- Complete Logic Loop: Transition from "Normal Driving" to "Accident Detected" based on physical sensor thresholds.
- Localization: Working GIS mapping of the accident site in Coimbatore.
- Service Integration: Functional dispatching logic for hospitals and police alerts.

Future Enhancements

- Traffic Signal Preemption: Implement "Green Corridor" logic to automatically clear traffic signals along the ambulance's GPS route.
- Live Sensor Integration: Connect the physical MPU6050 Accelerometer and Neo-6M GPS hardware modules.