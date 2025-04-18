import streamlit as st
import pandas as pd
import datetime
import random
from assets.quotes import motivational_quotes
from utils.data_utils import initialize_session_state, save_user_data, get_random_quote

# Page configuration
st.set_page_config(
    page_title="Mental Wellness Tracker",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
initialize_session_state()

# Main dashboard page
def main():
    # Header
    st.markdown("<h1 style='text-align: center;'>Mental Wellness Tracker</h1>", unsafe_allow_html=True)
    
    # Welcome message
    col1, col2 = st.columns([3, 1])
    with col1:
        if "user_name" in st.session_state and st.session_state["user_name"]:
            st.markdown(f"## Welcome back, {st.session_state['user_name']}! 👋")
        else:
            name_input = st.text_input("What's your name?", key="name_input_field")
            if name_input:
                st.session_state["user_name"] = name_input
                st.rerun()
            st.markdown("## Welcome to your Mental Wellness Journey! 👋")
    
    # Daily quote 
    st.markdown("### ✨ Quote of the Day")
    quote, author = get_random_quote()
    st.markdown(f"> *{quote}*")
    st.markdown(f"*— {author}*")
    
    # Mood tracker snapshot (if data exists)
    st.markdown("### 📊 Your Mental Wellness Snapshot")
    
    if len(st.session_state.get("mood_data", [])) > 0:
        # Get the most recent entry
        latest_entry = st.session_state["mood_data"][-1]
        
        col1, col2, col3 = st.columns(3)
        
        # Mood score column
        with col1:
            mood_emoji = "😄" if latest_entry["mood"] >= 4 else "🙂" if latest_entry["mood"] >= 3 else "😐" if latest_entry["mood"] >= 2 else "😔"
            mood_color = "#28a745" if latest_entry["mood"] >= 4 else "#17a2b8" if latest_entry["mood"] >= 3 else "#ffc107" if latest_entry["mood"] >= 2 else "#dc3545"
            st.markdown(f"""
            <div style='background-color: {mood_color}; padding: 10px; border-radius: 10px; text-align: center;'>
                <h3 style='color: white;'>Mood Score</h3>
                <p style='font-size: 36px; margin: 0;'>{mood_emoji}</p>
                <p style='color: white;'>{latest_entry['mood']}/5</p>
            </div>
            """, unsafe_allow_html=True)
            
        # Stress level column
        with col2:
            stress_emoji = "😌" if latest_entry.get("stress", 3) <= 2 else "😬" if latest_entry.get("stress", 3) <= 3 else "😰"
            stress_color = "#28a745" if latest_entry.get("stress", 3) <= 2 else "#ffc107" if latest_entry.get("stress", 3) <= 3 else "#dc3545"
            st.markdown(f"""
            <div style='background-color: {stress_color}; padding: 10px; border-radius: 10px; text-align: center;'>
                <h3 style='color: white;'>Stress Level</h3>
                <p style='font-size: 36px; margin: 0;'>{stress_emoji}</p>
                <p style='color: white;'>{latest_entry.get('stress', 3)}/5</p>
            </div>
            """, unsafe_allow_html=True)
            
        # Sleep rating column
        with col3:
            sleep_emoji = "😴" if latest_entry.get("sleep", 3) >= 4 else "🛌" if latest_entry.get("sleep", 3) >= 3 else "😫"
            sleep_color = "#28a745" if latest_entry.get("sleep", 3) >= 4 else "#17a2b8" if latest_entry.get("sleep", 3) >= 3 else "#dc3545"
            st.markdown(f"""
            <div style='background-color: {sleep_color}; padding: 10px; border-radius: 10px; text-align: center;'>
                <h3 style='color: white;'>Sleep Quality</h3>
                <p style='font-size: 36px; margin: 0;'>{sleep_emoji}</p>
                <p style='color: white;'>{latest_entry.get('sleep', 3)}/5</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Display the last check-in time
        st.caption(f"Last check-in: {latest_entry['date']}")
        
    else:
        st.info("No data yet. Complete your first mental health check to see your stats here.")
    
    # Call to action
    st.markdown("### 🎯 Let's Begin Your Journey Today")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if st.button("Take Today's Mental Health Check", use_container_width=True, type="primary"):
            st.switch_page("pages/1_Questionnaire.py")
    
    # Social media platforms that affect mental health
    st.markdown("### 📱 Track Your Digital Wellness")
    st.write("Select platforms that impact your mental wellbeing:")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        instagram = st.button("Instagram 📸", use_container_width=True)
        if instagram:
            st.session_state["selected_platform"] = "Instagram"
            st.switch_page("pages/1_Questionnaire.py")
            
    with col2:
        twitter = st.button("Twitter/X 🐦", use_container_width=True)
        if twitter:
            st.session_state["selected_platform"] = "Twitter"
            st.switch_page("pages/1_Questionnaire.py")
            
    with col3:
        facebook = st.button("Facebook 👥", use_container_width=True)
        if facebook:
            st.session_state["selected_platform"] = "Facebook"
            st.switch_page("pages/1_Questionnaire.py")
            
    with col4:
        youtube = st.button("YouTube 🎬", use_container_width=True)
        if youtube:
            st.session_state["selected_platform"] = "YouTube"
            st.switch_page("pages/1_Questionnaire.py")

if __name__ == "__main__":
    main()
