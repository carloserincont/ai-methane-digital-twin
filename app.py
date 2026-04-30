# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 21:41:53 2026

@author: LENOVO
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import time

# --------------------------
# CONFIG
# --------------------------
st.set_page_config(page_title="Methane Digital Twin", layout="wide")

st.title("Methane Emission Digital Twin (AI Prototype)")

# --------------------------
# SIMULATED DATA FUNCTION
# --------------------------
def generate_data():
    base = np.random.normal(50, 5)
    leak = np.random.choice([0, 1], p=[0.9, 0.1])
    
    if leak:
        return base + np.random.uniform(40, 100)
    return base

# --------------------------
# SESSION STATE INIT
# --------------------------
if "data" not in st.session_state:
    st.session_state.data = []

# --------------------------
# PRELOAD DATA (para que no se vea vacío)
# --------------------------
if len(st.session_state.data) < 50:
    for _ in range(50):
        st.session_state.data.append({
            "time": datetime.now(),
            "CH4": generate_data()
        })

# --------------------------
# ADD NEW DATA (SIMULACIÓN EN VIVO)
# --------------------------
new_value = generate_data()
timestamp = datetime.now()

st.session_state.data.append({
    "time": timestamp,
    "CH4": new_value
})

df = pd.DataFrame(st.session_state.data)

# --------------------------
# KPIs (ESTILO STARTUP)
# --------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Current CH4", f"{df.iloc[-1]['CH4']:.2f}")
col2.metric("Max CH4", f"{df['CH4'].max():.2f}")
col3.metric("Events Detected", int((df['CH4'] > 80).sum()))

# --------------------------
# STATUS INDICATOR
# --------------------------
latest = df.iloc[-1]

if latest["CH4"] > 80:
    st.error("🚨 Methane Leak Detected – Immediate Action Required")
elif latest["CH4"] > 65:
    st.warning("⚠️ Elevated Methane Levels")
else:
    st.success("✅ System Stable")

# --------------------------
# GRAPH (PRO)
# --------------------------
fig = px.line(df, x="time", y="CH4", title="Real-Time Methane Emissions")

fig.update_layout(
    xaxis_title="Time",
    yaxis_title="CH4 Concentration",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------
# EVENT TABLE
# --------------------------
st.subheader("Detected Emission Events")

events = df[df["CH4"] > 80]

st.dataframe(events)

# --------------------------
# REPORT GENERATOR
# --------------------------
st.subheader("Verification Engine")

if st.button("Generate Verification Report"):
    if len(events) == 0:
        st.info("No emission events detected.")
    else:
        last_event = events.iloc[-1]
        impact = last_event["CH4"] * 0.086
        
        report = f"""
Methane Emission Verification Report

Timestamp: {last_event['time']}
CH4 Level: {last_event['CH4']:.2f}
Status: Confirmed Leak
Estimated CO2-equivalent Impact: {impact:.2f}

System: AI Digital Twin Prototype
"""
        st.download_button(
            label="Download Report",
            data=report,
            file_name="verification_report.txt"
        )

# --------------------------
# AUTO-REFRESH (SIMULACIÓN EN TIEMPO REAL)
# --------------------------
time.sleep(1)
st.rerun()