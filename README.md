 G-Trace:

G-Trace is a prototype smart accident detection and rescue system that simulates how accidents can be detected, locations shared, hospitals notified, and traffic cleared for ambulance movement.

PROBLEM STATEMENT:

Road accidents can cause delays in emergency response due to slow detection, unawareness of hospital availability, and traffic congestion. Existing solutions rarely simulate the complete pipeline from detection to rescue.

OUR IDEA:

G-Trace simulates the full emergency response system:

* Detect accidents using accelerometer impact simulation  
* Show GPS location of the accident on a dashboard  
* Notify the nearest hospital and simulate ambulance dispatch  
* Display emergency alerts and clear traffic signals  

This helps learners and evaluators understand how IoT and automation can improve emergency response time.

MINI PROTOTYPE:

For this prototype, the system focuses on:

* Simulated accident detection using a slider (impact intensity)  
* GPS location display for a single accident scenario  
* Display of three nearby hospitals with automatic selection of the nearest  
* Emergency alert panel showing accident, ambulance dispatch, and traffic control  
* Minimal dashboard UI using Streamlit  

The goal is to demonstrate the concept of automated accident detection and emergency response.


TECH STACK:

* Python  
* Streamlit  
* Pandas  

PROJECT STURTURE:

```
gtrace-project/
├── app.py              # Main application integrating all modules
├── member1.py          # Controls & accident detection
├── member2.py          # Dashboard header
├── member3.py          # GPS tracking map
├── member4.py          # Hospital dispatch system
├── member5.py          # Alerts & traffic simulation
```
HOW TO RUN THE APP:

1. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

2. ACTIVATE THE ENVIRONMENT:

   ```bash
   .\venv\Scripts\Activate
   ```

3. INSTALL DEPENDENCIES:

   ```bash
   pip install streamlit pandas

4. RUN THE APP:

   ```bash
   streamlit run app.py

 TEAM CONTRIBUTION:

Each team member worked on a separate module:

* member1.py – Controls and accident detection logic  
* member2.py – Dashboard header and system status  
* member3.py – GPS location map  
* member4.py – Hospital dispatch system  
* member5.py – Emergency alerts and traffic simulation  

FUTURE WORK:

* Integrate real accelerometer sensors for actual accident detection  
* Use live GPS for real-time tracking  
* Connect to hospital APIs for automatic notifications  
* Implement real-time traffic control via IoT devices  
* Extend system to mobile emergency apps for on-the-go monitoring
