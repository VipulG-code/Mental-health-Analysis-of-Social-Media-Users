import streamlit as st
import pandas as pd
import datetime
import random
import os
from assets.quotes import motivational_quotes
from utils.data_utils import initialize_session_state, save_user_data, get_random_quote, export_user_data_csv

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
    # Check if user is authenticated
    if not st.session_state.get("authenticated", False):
        st.switch_page("pages/0_Login.py")
    
    # Header
    st.markdown("<h1 style='text-align: center;'>Mental Wellness Tracker</h1>", unsafe_allow_html=True)
    
    # Welcome message
    col1, col2 = st.columns([3, 1])
    with col1:
        if "user_name" in st.session_state and st.session_state["user_name"]:
            st.markdown(f"## Welcome back, {st.session_state['user_name']}! 👋")
        else:
            st.markdown("## Welcome to your Mental Wellness Journey! 👋")
    
    with col2:
        if st.button("Logout", key="logout"):
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            
            # Re-initialize session state
            initialize_session_state()
            
            # Redirect to login page
            st.switch_page("pages/0_Login.py")
    
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
            mood_value = latest_entry.get("mood", 3)
            mood_emoji = "😄" if mood_value >= 4 else "🙂" if mood_value >= 3 else "😐" if mood_value >= 2 else "😔"
            mood_color = "#28a745" if mood_value >= 4 else "#17a2b8" if mood_value >= 3 else "#ffc107" if mood_value >= 2 else "#dc3545"
            st.markdown(f"""
            <div style='background-color: {mood_color}; padding: 10px; border-radius: 10px; text-align: center;'>
                <h3 style='color: white;'>Mood Score</h3>
                <p style='font-size: 36px; margin: 0;'>{mood_emoji}</p>
                <p style='color: white;'>{mood_value}/5</p>
            </div>
            """, unsafe_allow_html=True)
            
        # Stress level column
        with col2:
            stress_value = latest_entry.get("stress", 3)
            stress_emoji = "😌" if stress_value <= 2 else "😬" if stress_value <= 3 else "😰"
            stress_color = "#28a745" if stress_value <= 2 else "#ffc107" if stress_value <= 3 else "#dc3545"
            st.markdown(f"""
            <div style='background-color: {stress_color}; padding: 10px; border-radius: 10px; text-align: center;'>
                <h3 style='color: white;'>Stress Level</h3>
                <p style='font-size: 36px; margin: 0;'>{stress_emoji}</p>
                <p style='color: white;'>{stress_value}/5</p>
            </div>
            """, unsafe_allow_html=True)
            
        # Sleep rating column
        with col3:
            sleep_value = latest_entry.get("sleep", 3)
            sleep_emoji = "😴" if sleep_value >= 4 else "🛌" if sleep_value >= 3 else "😫"
            sleep_color = "#28a745" if sleep_value >= 4 else "#17a2b8" if sleep_value >= 3 else "#dc3545"
            st.markdown(f"""
            <div style='background-color: {sleep_color}; padding: 10px; border-radius: 10px; text-align: center;'>
                <h3 style='color: white;'>Sleep Quality</h3>
                <p style='font-size: 36px; margin: 0;'>{sleep_emoji}</p>
                <p style='color: white;'>{sleep_value}/5</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Display the last check-in time
        st.caption(f"Last check-in: {latest_entry['date']}")
        
        # Display ML score if available
        if "ml_wellbeing_score" in latest_entry:
            st.markdown("### 🤖 ML-Based Wellbeing Analysis")
            ml_score = latest_entry["ml_wellbeing_score"]
            
            # Determine score color and label
            if ml_score >= 80:
                score_color = "#28a745"
                score_label = "Excellent"
            elif ml_score >= 60:
                score_color = "#17a2b8"
                score_label = "Good"
            elif ml_score >= 40:
                score_color = "#ffc107"
                score_label = "Fair"
            else:
                score_color = "#dc3545"
                score_label = "Needs Attention"
            
            st.markdown(f"""
            <div style='background-color: {score_color}; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;'>
                <h4 style='color: white; margin-top: 0;'>Your Personalized Wellbeing Score</h4>
                <p style='font-size: 42px; margin: 0; font-weight: bold; color: white;'>{ml_score}</p>
                <p style='color: white; margin-bottom: 0;'>{score_label}</p>
            </div>
            """, unsafe_allow_html=True)
        
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
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
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
    
    with col5:
        snapchat = st.button("Snapchat 👻", use_container_width=True)
        if snapchat:
            st.session_state["selected_platform"] = "Snapchat"
            st.switch_page("pages/1_Questionnaire.py")
    
    # User data management section
    st.markdown("---")
    st.markdown("### 💾 Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export Your Data (CSV)", use_container_width=True):
            export_path = export_user_data_csv()
            if export_path:
                with open(export_path, "rb") as file:
                    st.download_button(
                        label="Download CSV",
                        data=file,
                        file_name=os.path.basename(export_path),
                        mime="text/csv"
                    )
            else:
                st.error("No data to export or export failed")
    
    with col2:
        if st.button("View Progress Tracker", use_container_width=True):
            st.switch_page("pages/3_Progress_Tracker.py")

if __name__ == "__main__":
    main()
