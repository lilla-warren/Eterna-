# 🌿 ETERNA 2.0 - Ultimate AI Energy Companion
# 🚀 Streamlit App - Full Code

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import time
import pytz
import random

# ========================
# 🏗️ CORE SYSTEM SETUP
# ========================
class EnergyAI:
    def __init__(self):
        self.learned_habits = {}
        self.peak_hours = (18, 22)
        self.energy_rates = {
            'peak': 0.65,    # AED/kWh
            'off_peak': 0.30 # AED/kWh
        }
        
    def detect_usage_patterns(self, history):
        """AI that learns user habits from historical data"""
        if len(history) > 3:
            avg_ac = np.mean([x['AC'] for x in history[-3:]])
            if avg_ac > 2.8 and 'high_ac' not in self.learned_habits:
                self.learned_habits['high_ac'] = True
                
    def get_smart_suggestions(self, current_usage, user_prefs):
        """Generates hyper-personalized recommendations"""
        now = datetime.now(pytz.timezone('Asia/Dubai'))
        suggestions = []
        
        # Time-based intelligence
        if now.hour in self.peak_hours and current_usage['Appliances'] > 0.7:
            savings = round((current_usage['Appliances'] * (self.energy_rates['peak'] - self.energy_rates['off_peak'])), 2)
            suggestions.append(f"🚨 Peak hours! Delay appliances to save {savings} AED")
        
        # Learned habit adjustments
        if self.learned_habits.get('high_ac'):
            suggestions.append("🌡️ AC Usage Pattern Detected: Consider smart thermostat")
        
        return suggestions or ["🌟 Your usage looks optimal!"]

# ========================
# 📊 DATA ENGINE
# ========================
def generate_usage_history(days=7):
    """Generates realistic historical data"""
    history = []
    now = datetime.now()
    
    for day in range(days, -1, -1):
        date = now - timedelta(days=day)
        for hour in range(24):
            # Daily patterns
            if 6 <= hour <= 8:  # Morning
                ac = random.uniform(1.8, 2.5)
                lights = random.uniform(0.4, 0.7)
            elif 18 <= hour <= 22:  # Evening
                ac = random.uniform(2.5, 3.2)
                lights = random.uniform(0.6, 0.9)
            else:  # Night
                ac = random.uniform(0.8, 1.5) * 0.6
                lights = random.uniform(0.1, 0.3)
            
            history.append({
                'timestamp': date.replace(hour=hour, minute=0),
                'AC': round(ac, 2),
                'Lights': round(lights, 2),
                'Appliances': round(random.uniform(0.5, 1.2), 2)
            })
    
    return history

# ========================
# 🎨 UI COMPONENTS
# ========================
def create_gauge(value, title):
    """Creates beautiful gauge charts"""
    fig = px.pie(
        values=[value, 100-value],
        names=['Used', 'Remaining'],
        hole=0.7,
        color_discrete_sequence=['#00cc96', 'lightgray']
    )
    fig.update_layout(
        showlegend=False,
        annotations=[{'text': f"{value}%", 'font_size': 20}],
        title=title
    )
    return fig

# ========================
# 🚀 APP CORE
# ========================
def main():
    # Initialize everything
    st.set_page_config(
        page_title="Eterna 2.0",
        page_icon="⚡",
        layout="wide"
    )
    
    if 'ai' not in st.session_state:
        st.session_state.ai = EnergyAI()
        st.session_state.history = generate_usage_history()
        st.session_state.prefs = {
            'name': 'User',
            'comfort': 'Balanced',
            'budget': 300
        }
    
    # ===== SIDEBAR =====
    with st.sidebar:
        st.title("⚙️ Settings")
        st.session_state.prefs['name'] = st.text_input("Name", st.session_state.prefs['name'])
        st.selectbox("Comfort Profile", ["Eco", "Balanced", "Comfort"], key="comfort")
        st.slider("Monthly Budget (AED)", 100, 1000, key="budget")
    
    # ===== MAIN DASHBOARD =====
    st.title(f"🌿 Eterna 2.0 • Welcome, {st.session_state.prefs['name']}!")
    
    # Current Usage
    current = st.session_state.history[-1]
    total = sum([current['AC'], current['Lights'], current['Appliances']])
    
    cols = st.columns(4)
    cols[0].metric("Usage", f"{total} kWh")
    cols[1].metric("Cost", f"{total*0.5:.2f} AED")
    cols[2].metric("CO₂ Saved", f"{total*0.42:.2f} kg")
    cols[3].metric("Water Saved", f"{total*4.2:.2f} L")
    
    # AI Recommendations
    st.session_state.ai.detect_usage_patterns(st.session_state.history)
    suggestions = st.session_state.ai.get_smart_suggestions(current, st.session_state.prefs)
    
    with st.expander("💡 AI Recommendations", expanded=True):
        for s in suggestions:
            st.success(s)
    
    # Visualization
    tab1, tab2 = st.tabs(["📈 Trends", "🎛️ Simulator"])
    
    with tab1:
        df = pd.DataFrame(st.session_state.history[-24:])
        st.plotly_chart(px.line(df, x='timestamp', y=['AC', 'Lights', 'Appliances']), use_container_width=True)
    
    with tab2:
        st.write("Test different scenarios:")
        ac = st.slider("AC Usage", 0.5, 5.0, current['AC'])
        if st.button("Simulate"):
            sim_usage = {'AC': ac, 'Lights': current['Lights'], 'Appliances': current['Appliances']}
            sim_suggestions = st.session_state.ai.get_smart_suggestions(sim_usage, st.session_state.prefs)
            for s in sim_suggestions:
                st.info(f"🔮 {s}")

if __name__ == "__main__":
    main()
