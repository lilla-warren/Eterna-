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

def generate_mock_usage():
    return {
        "AC": round(random.uniform(1.5, 3.0), 2),
        "Lights": round(random.uniform(0.3, 0.6), 2),
        "Appliances": round(random.uniform(0.5, 1.0), 2)
    }

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

st.title("⚡ Eterna Dashboard")
if "user_prefs" in st.session_state and "name" in st.session_state.user_prefs:
    st.write(f"Welcome back, **{st.session_state.user_prefs['name']}**!")
else:
    st.write("Welcome back!")

st.header("🔌 Real-Time Energy Usage")
usage = generate_mock_usage()
total_usage = sum(usage.values())

st.session_state.usage_history.append(total_usage)

st.metric("Total Energy Used (kWh)", total_usage)
st.bar_chart(pd.DataFrame(usage.values(), index=usage.keys(), columns=["kWh"]))

# --- Azure ML Simulated Prediction ---
if len(st.session_state.usage_history) > 2:
    predicted = train_and_predict_energy(st.session_state.usage_history)
    st.info(f"🔮 Predicted Tomorrow's Energy Usage (via Azure ML): **{predicted} kWh**")

# --- 3. Smart Advisor ---
st.header("🧠 Smart Suggestions")
suggestions = get_ai_suggestions(usage, st.session_state.user_prefs)
arabic_mode = st.checkbox("🔁 Show Arabic Suggestions")

translations = {
    "Turn off AC in Room 2 — no activity detected.": "أطفئ التكييف في الغرفة 2 — لا يوجد نشاط.",
    "Fan + 1° higher AC temp = same comfort, lower cost.": "استخدم المروحة وارفع حرارة التكييف بدرجة واحدة — نفس الراحة وتكلفة أقل.",
    "Delay laundry to off-peak hours (saves 1.5 AED).": "أجل الغسيل إلى ساعات خارج الذروة لتوفير 1.5 درهم.",
    "Switch to eco-mode lighting in hallways.": "فعّل وضع الإضاءة الاقتصادية في الممرات."
}

for s in suggestions:
    st.success("💡 " + (translations[s] if arabic_mode and s in translations else s))

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
    st.info("🤖 " + (translations[s] if arabic_mode and s in translations else s))

st.caption("🔁 Powered by Eterna AI — Predict. Advise. Save.")
