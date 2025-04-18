import streamlit as st
import pandas as pd
import altair as alt
from utils.data_utils import initialize_session_state, get_mood_data_as_df
from utils.ui_utils import display_wellbeing_score

# Page configuration
st.set_page_config(
    page_title="Re-Evaluation | Mental Wellness Tracker",
    page_icon="🌱",
    layout="wide"
)

# Initialize session state
initialize_session_state()

def main():
    st.markdown("<h1 style='text-align: center;'>Re-Evaluation</h1>", unsafe_allow_html=True)
    
    # Check if we have enough mood data
    if not st.session_state.get("mood_data", []) or len(st.session_state["mood_data"]) < 1:
        st.warning("You need to complete at least one assessment before re-evaluation.")
        if st.button("Go to Questionnaire"):
            st.switch_page("pages/1_Questionnaire.py")
        return
    
    # Top section: Timeline
    st.subheader("Ready for a quick reassessment? 👀")
    
    # Get mood data
    df = get_mood_data_as_df()
    
    if not df.empty:
        # Create a timeline of previous evaluations
        st.write("Your previous evaluations:")
        
        # Format the date column for display
        if 'date' in df.columns:
            df['formatted_date'] = pd.to_datetime(df['date']).dt.strftime('%b %d, %Y')
        
        # Create a horizontal timeline
        dates = df['formatted_date'].tolist() if 'formatted_date' in df.columns else []
        
        if dates:
            # Visual timeline
            timeline_html = """
            <div style="display: flex; justify-content: space-between; align-items: center; margin: 20px 0;">
            """
            
            for i, date in enumerate(dates):
                # Color the most recent entry differently
                color = "#6C5CE7" if i == len(dates) - 1 else "#A0A0A0"
                timeline_html += f"""
                <div style="display: flex; flex-direction: column; align-items: center; flex: 1;">
                    <div style="width: 15px; height: 15px; border-radius: 50%; background-color: {color};"></div>
                    <div style="height: 2px; background-color: {color}; width: 100%; margin: 5px 0;"></div>
                    <div style="font-size: 12px; text-align: center;">{date}</div>
                </div>
                """
            
            timeline_html += "</div>"
            st.markdown(timeline_html, unsafe_allow_html=True)
    
    # Middle section: Re-evaluation options
    st.markdown("---")
    st.subheader("Choose what to reassess")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px; height: 100%;">
            <h3>✅ General Mood Check</h3>
            <p>A quick assessment of your overall mental wellbeing right now.</p>
            <ul>
                <li>Current mood</li>
                <li>Sleep quality</li>
                <li>Stress levels</li>
                <li>Anxiety</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start General Assessment", use_container_width=True):
            st.session_state["current_step"] = 1
            st.session_state["current_responses"] = {}
            st.session_state["selected_platform"] = None
            st.switch_page("pages/1_Questionnaire.py")
    
    with col2:
        st.markdown("""
        <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px; height: 100%;">
            <h3>📱 Platform-Specific Quiz</h3>
            <p>Evaluate how a specific social platform is affecting your mental health.</p>
            <ul>
                <li>Platform usage</li>
                <li>Content impact</li>
                <li>Comparison feelings</li>
                <li>FOMO experiences</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Platform selection
        platforms = ["Instagram", "Twitter", "Facebook", "YouTube", "TikTok"]
        selected_platform = st.selectbox("Choose a platform", ["Select a platform"] + platforms)
        
        if selected_platform != "Select a platform":
            if st.button(f"Start {selected_platform} Assessment", use_container_width=True):
                st.session_state["current_step"] = 1
                st.session_state["current_responses"] = {}
                st.session_state["selected_platform"] = selected_platform
                st.switch_page("pages/1_Questionnaire.py")
    
    # Bottom section: Comparison (if enough data)
    if len(df) >= 2:
        st.markdown("---")
        st.subheader("Compare Your Results")
        
        # Allow user to select which assessments to compare
        if len(df) > 2:
            st.write("Select which assessments to compare:")
            assessment_options = df['formatted_date'].tolist() if 'formatted_date' in df.columns else [f"Assessment {i+1}" for i in range(len(df))]
            
            col1, col2 = st.columns(2)
            with col1:
                first_assessment = st.selectbox("First assessment", assessment_options[:-1], index=0)
                first_idx = assessment_options.index(first_assessment)
            
            with col2:
                second_assessment = st.selectbox("Second assessment", assessment_options[first_idx+1:], index=len(assessment_options[first_idx+1:])-1)
                second_idx = assessment_options.index(second_assessment)
        else:
            # If only 2 assessments, compare them directly
            first_idx, second_idx = 0, 1
        
        # Get the data for comparison
        first_data = df.iloc[first_idx].to_dict()
        second_data = df.iloc[second_idx].to_dict()
        
        # Create a side-by-side comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### First Assessment")
            st.caption(first_data.get('formatted_date', 'Unknown date'))
            display_wellbeing_score(first_data)
            
            # Display metrics
            if 'mood' in first_data:
                mood_mapping = {1: "Struggling 😢", 2: "Low 😔", 3: "Neutral 😐", 4: "Good 🙂", 5: "Great 😄"}
                st.metric("Mood", mood_mapping.get(first_data['mood'], "Unknown"))
            
            if 'sleep' in first_data:
                st.metric("Sleep Quality", f"{first_data['sleep']}/5")
            
            if 'stress' in first_data:
                st.metric("Stress Level", f"{first_data['stress']}/5")
            
            if 'anxiety' in first_data:
                anxiety_status = "Yes" if first_data['anxiety'] else "No"
                st.metric("Feeling Anxious", anxiety_status)
        
        with col2:
            st.markdown(f"### Current Assessment")
            st.caption(second_data.get('formatted_date', 'Unknown date'))
            display_wellbeing_score(second_data)
            
            # Display metrics with delta values
            if 'mood' in second_data and 'mood' in first_data:
                mood_mapping = {1: "Struggling 😢", 2: "Low 😔", 3: "Neutral 😐", 4: "Good 🙂", 5: "Great 😄"}
                mood_delta = second_data['mood'] - first_data['mood']
                st.metric("Mood", mood_mapping.get(second_data['mood'], "Unknown"), delta=mood_delta)
            
            if 'sleep' in second_data and 'sleep' in first_data:
                sleep_delta = second_data['sleep'] - first_data['sleep']
                st.metric("Sleep Quality", f"{second_data['sleep']}/5", delta=sleep_delta)
            
            if 'stress' in second_data and 'stress' in first_data:
                # Invert delta for stress (negative delta is good)
                stress_delta = first_data['stress'] - second_data['stress']
                st.metric("Stress Level", f"{second_data['stress']}/5", delta=stress_delta)
            
            if 'anxiety' in second_data and 'anxiety' in first_data:
                anxiety_status = "Yes" if second_data['anxiety'] else "No"
                # For anxiety, True (Yes) is worse than False (No)
                anxiety_change = not second_data['anxiety'] and first_data['anxiety']
                anxiety_worse = second_data['anxiety'] and not first_data['anxiety']
                anxiety_delta = "Improved" if anxiety_change else "Worse" if anxiety_worse else None
                st.metric("Feeling Anxious", anxiety_status, delta=anxiety_delta)
    
    # Navigation
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("View Progress Tracker", key="view_progress"):
            st.switch_page("pages/3_Progress_Tracker.py")
    
    with col2:
        if st.button("Get New AI Suggestions", key="new_suggestions"):
            # Clear existing suggestions to generate new ones
            st.session_state["ai_suggestions"] = []
            st.switch_page("pages/2_AI_Suggestions.py")

if __name__ == "__main__":
    main()
