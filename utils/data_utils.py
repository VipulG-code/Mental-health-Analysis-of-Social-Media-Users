import streamlit as st
import datetime
import pandas as pd
import random
from assets.quotes import motivational_quotes

def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if "user_name" not in st.session_state:
        st.session_state["user_name"] = ""
    
    if "mood_data" not in st.session_state:
        st.session_state["mood_data"] = []
    
    if "current_responses" not in st.session_state:
        st.session_state["current_responses"] = {}
    
    if "selected_platform" not in st.session_state:
        st.session_state["selected_platform"] = None
    
    if "ai_suggestions" not in st.session_state:
        st.session_state["ai_suggestions"] = []
        
    if "current_step" not in st.session_state:
        st.session_state["current_step"] = 1

def save_user_data(responses):
    """Save user response data to session state"""
    # Add timestamp
    responses["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Add to mood data array
    st.session_state["mood_data"].append(responses)
    
    # Clear current responses
    st.session_state["current_responses"] = {}
    st.session_state["current_step"] = 1

def get_mood_data_as_df():
    """Convert mood data to pandas DataFrame for visualization"""
    if not st.session_state.get("mood_data", []):
        return pd.DataFrame()
    
    df = pd.DataFrame(st.session_state["mood_data"])
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    return df

def get_random_quote():
    """Return a random motivational quote"""
    quote_entry = random.choice(motivational_quotes)
    return quote_entry["quote"], quote_entry["author"]

def calculate_wellbeing_score(data):
    """Calculate an overall wellbeing score based on mood data"""
    if not data or len(data) == 0:
        return 0
    
    # Extract relevant metrics
    mood = data.get('mood', 3)
    sleep = data.get('sleep', 3)
    stress = 6 - data.get('stress', 3)  # Invert stress so higher is better
    anxiety = 0 if data.get('anxiety', False) else 1  # 0 if anxious, 1 if not
    
    # Calculate weighted average (adjust weights as needed)
    wellbeing_score = (mood * 0.4) + (sleep * 0.3) + (stress * 0.2) + (anxiety * 0.1)
    
    # Convert to 0-100 scale
    return round((wellbeing_score / 5) * 100)
