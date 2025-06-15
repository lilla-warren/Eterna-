# Eterna: AI-Powered Smart Energy Advisor
# Streamlit-based prototype with enhanced features

import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime

# --- Constants & Configuration ---
DEFAULT_PREFS = {
    "name": "",
    "home_size": "2BHK",
    "working_hours": 8,
    "ac_temp": 24,
    "eco_mode": True
}

# --- Mock Data Generation ---
def generate_mock_usage():
    """Generate realistic mock energy usage data"""
    current_hour = datetime.now().hour
    night_multiplier = 0.7 if 22 <= current_hour <= 6 else 1.0
    
    return {
        "AC": round(random.uniform(1.5, 3.0) * night_multiplier, 2),
        "Lights": round(random.uniform(0.3, 0.6) * night_multiplier, 2),
        "Appliances": round(random.uniform(0.5, 1.0) * (1.5 if 18 <= current_hour <= 22 else 1.0), 2)
    }

def get_ai_suggestions(usage, prefs):
    """Generate intelligent suggestions based on usage patterns"""
    suggestions = []
    current_hour = datetime.now().hour
    
    # AC-related suggestions
    if usage["AC"] > 2.5:
        suggestions.append("Turn off AC in unoccupied rooms — no activity detected.")
        if prefs["ac_temp"] < 26:
            suggestions.append(f"Try increasing AC temperature to {prefs['ac_temp']+1}°C (saves ~0.8 kWh/hour)")
    
    # Time-based suggestions
    if 8 <= current_hour <= 11 and usage["Appliances"] > 0.7:
        suggestions.append("Delay laundry to off-peak hours (after 8PM saves ~1.5 AED)")
    
    # Eco-mode suggestions
    if prefs.get("eco_mode"):
        if usage["Lights"] > 0.5:
            suggestions.append("Switch to eco-mode lighting in common areas (saves ~0.2 kWh/hour)")
    
    # General suggestions
    if len(suggestions) < 2:
        suggestions.append("Consider smart plugs for idle electronics (potential 10% savings)")
    
    return suggestions

# --- Initialize Session State ---
def init_session_state():
    if "registered" not in st.session_state:
        st.session_state.registered = False
    if "user_prefs" not in st.session_state:
        st.session_state.user_prefs = DEFAULT_PREFS.copy()

# --- User Onboarding ---
def show_onboarding():
    st.title("🌱 Welcome to Eterna")
    st.subheader("AI-powered energy optimization for your home")
    
    with st.form("user_form"):
        name = st.text_input("Your Name", value=st.session_state.user_prefs["name"])
        home_size = st.selectbox(
            "Home Size", 
            ["Studio", "1BHK", "2BHK", "3BHK", "Villa"],
            index=["Studio", "1BHK", "2BHK", "3BHK", "Villa"].index(st.session_state.user_prefs["home_size"])
        )
        working_hours = st.slider(
            "Your Daily Working Hours", 
            0, 24, 
            st.session_state.user_prefs["working_hours"]
        )
        ac_pref = st.slider(
            "Preferred Room Temperature (°C)", 
            20, 30, 
            st.session_state.user_prefs["ac_temp"]
        )
        eco_mode = st.checkbox(
            "Enable Eco Mode (recommended)", 
            value=st.session_state.user_prefs["eco_mode"]
        )
        
        submitted = st.form_submit_button("Start Optimizing")
    
    if submitted and name:
        st.session_state.user_prefs = {
            "name": name,
            "home_size": home_size,
            "working_hours": working_hours,
            "ac_temp": ac_pref,
            "eco_mode": eco_mode
        }
        st.session_state.registered = True
        st.success(f"Welcome, {name}! Setting up your personalized dashboard...")
        time.sleep(1)
        st.rerun()

# --- Main Dashboard ---
def show_dashboard():
    # Sidebar Settings
    st.sidebar.title("⚙️ Settings")
    if st.sidebar.button("Reset Preferences"):
        st.session_state.registered = False
        st.rerun()
    
    # Header with personalized greeting
    st.title(f"⚡ Eterna Dashboard")
    st.write(f"Hello, **{st.session_state.user_prefs['name']}**! Here's your energy overview.")
    
    # Real-Time Usage Section
    st.header("🔌 Current Energy Usage")
    usage = generate_mock_usage()
    total_usage = sum(usage.values())
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Consumption", f"{total_usage} kWh")
    with col2:
        st.metric("Estimated Cost", f"{total_usage * 0.5:.2f} AED")
    
    st.bar_chart(pd.DataFrame.from_dict(usage, orient='index', columns=['kWh']))
    
    # AI Suggestions Section
    st.header("🧠 Smart Recommendations")
    suggestions = get_ai_suggestions(usage, st.session_state.user_prefs)
    
    if not suggestions:
        st.info("No specific recommendations right now. Your usage looks efficient!")
    else:
        for i, suggestion in enumerate(suggestions, 1):
            st.success(f"{i}. {suggestion}")
    
    # Impact Metrics
    st.header("🌍 Your Sustainability Impact")
    savings = round(total_usage * random.uniform(0.5, 1.5), 2)
    carbon_saved = round(total_usage * 0.42, 2)
    
    cols = st.columns(3)
    cols[0].metric("💰 Savings", f"{savings} AED")
    cols[1].metric("🌱 CO₂ Saved", f"{carbon_saved} kg")
    cols[2].metric("💧 Water Saved", f"{carbon_saved * 10} liters")
    
    # Simulation Tool
    st.header("🧪 Usage Simulator")
    with st.expander("Try different scenarios"):
        sim_ac = st.slider("AC Usage (kWh)", 0.5, 5.0, usage["AC"])
        sim_lights = st.slider("Lights Usage (kWh)", 0.1, 1.0, usage["Lights"])
        sim_appliances = st.slider("Appliances Usage (kWh)", 0.1, 2.0, usage["Appliances"])
        
        if st.button("Calculate Savings"):
            sim_usage = {"AC": sim_ac, "Lights": sim_lights, "Appliances": sim_appliances}
            sim_suggestions = get_ai_suggestions(sim_usage, st.session_state.user_prefs)
            
            st.write("**Potential Savings:**")
            for s in sim_suggestions:
                st.info(f"• {s}")

# --- Main App Flow ---
def main():
    st.set_page_config(
        page_title="Eterna Energy Advisor",
        page_icon="⚡",
        layout="centered"
    )
    
    init_session_state()
    
    if not st.session_state.registered:
        show_onboarding()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
