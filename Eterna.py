#Eterna: AI-Powered Smart Energy Advisor
# Streamlit-based prototype

import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime

# --- Mock Data & Settings ---
def generate_mock_usage():
    return {
        "AC": round(random.uniform(1.5, 3.0), 2),
        "Lights": round(random.uniform(0.3, 0.6), 2),
        "Appliances": round(random.uniform(0.5, 1.0), 2)
    }

def get_ai_suggestions(usage, prefs):
    suggestions = []
    if usage["AC"] > 2.5:
        suggestions.append("Turn off AC in Room 2 — no activity detected.")
        suggestions.append("Fan + 1° higher AC temp = same comfort, lower cost.")
    if datetime.now().hour < 12:
        suggestions.append("Delay laundry to off-peak hours (saves 1.5 AED).")
    if prefs.get("eco_mode"):
        suggestions.append("Switch to eco-mode lighting in hallways.")
    return suggestions

# --- Session State for User Info ---
if "registered" not in st.session_state:
    st.session_state.registered = False
if "user_prefs" not in st.session_state:
    st.session_state.user_prefs = {}

# --- 1. User Onboarding & Setup ---
if not st.session_state.registered:
    st.title("🌱 Welcome to Eterna")
    st.subheader("Smarter energy. Every day.")

    with st.form("user_form"):
        name = st.text_input("Your Name")
        home_size = st.selectbox("Home Size", ["Studio", "1BHK", "2BHK", "Villa"])
        working_hours = st.slider("Your Daily Working Hours", 0, 24, 8)
        ac_pref = st.slider("Preferred Room Temperature (°C)", 20, 30, 24)
        eco_mode = st.checkbox("Enable Eco Mode")
        submit = st.form_submit_button("Start Saving")

    if submit:
        st.session_state.user_prefs = {
            "name": name,
            "home_size": home_size,
            "working_hours": working_hours,
            "ac_temp": ac_pref,
            "eco_mode": eco_mode
        }
        st.session_state.registered = True
        st.success("Welcome, " + name + "! Eterna is setting up your dashboard...")
        time.sleep(1)
        st.experimental_rerun()
else:
    # --- 2. Real-Time Energy Dashboard ---
    st.sidebar.title("⚙️ Settings")
    if st.sidebar.button("Reset Setup"):
        st.session_state.registered = False
        st.experimental_rerun()

    st.title("⚡ Eterna Dashboard")
    st.write("Welcome back, **{}**!".format(st.session_state.user_prefs["name"]))

    st.header("🔌 Real-Time Energy Usage")
    usage = generate_mock_usage()
    total_usage = sum(usage.values())

    st.metric("Total Energy Used (kWh)", total_usage)
    st.bar_chart(pd.DataFrame(usage.values(), index=usage.keys(), columns=["kWh"]))

    # --- 3. Smart Advisor ---
    st.header("🧠 Smart Suggestions")
    suggestions = get_ai_suggestions(usage, st.session_state.user_prefs)
    for s in suggestions:
        st.success("💡 " + s)

    # --- 4. Impact & Rewards ---
    st.header("🌍 Impact & Rewards")
    savings = round(total_usage * random.uniform(0.5, 1.5), 2)
    carbon_saved = round(total_usage * 0.42, 2)
    trees_equivalent = round(carbon_saved / 20, 2)

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 AED Saved", f"{savings}")
    col2.metric("🌱 CO₂ Saved (kg)", f"{carbon_saved}")
    col3.metric("🌳 Trees Equivalent", f"{trees_equivalent}")

    st.progress(min(1.0, savings / 10))
    st.caption("Reach 10 AED to earn your next 🌟")

    # --- 5. Simulation Mode ---
    st.header("🧪 Simulation Mode")
    sim_ac = st.slider("AC Usage (kWh)", 0.5, 5.0, usage["AC"])
    sim_lights = st.slider("Lights Usage (kWh)", 0.1, 1.0, usage["Lights"])
    sim_appliances = st.slider("Appliances Usage (kWh)", 0.1, 2.0, usage["Appliances"])

    sim_total = sim_ac + sim_lights + sim_appliances
    st.write(f"Total Simulated Usage: **{sim_total} kWh**")
    st.write("AI would recommend:")
    sim_suggestions = get_ai_suggestions({"AC": sim_ac, "Lights": sim_lights, "Appliances": sim_appliances}, st.session_state.user_prefs)
    for s in sim_suggestions:
        st.info("🤖 " + s)

    st.caption("🔁 Powered by Eterna AI — Predict. Advise. Save.")
