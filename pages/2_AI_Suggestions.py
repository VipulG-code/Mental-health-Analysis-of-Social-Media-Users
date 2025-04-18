import streamlit as st
from utils.data_utils import initialize_session_state
from utils.openai_utils import generate_wellness_suggestions
from utils.ui_utils import display_wellbeing_score

# Page configuration
st.set_page_config(
    page_title="AI Suggestions | Mental Wellness Tracker",
    page_icon="🌱",
    layout="wide"
)

# Initialize session state
initialize_session_state()

def main():
    st.markdown("<h1 style='text-align: center;'>AI-Based Suggestions</h1>", unsafe_allow_html=True)
    
    # Check if we have mood data
    if not st.session_state.get("mood_data", []):
        st.warning("You haven't completed a mental health check yet. Please take a survey first.")
        if st.button("Go to Questionnaire"):
            st.switch_page("pages/1_Questionnaire.py")
        return
    
    # Get the most recent entry
    latest_entry = st.session_state["mood_data"][-1]
    
    # Top section: Mood Summary
    st.subheader("Your Mental Snapshot")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Display wellbeing score
        wellbeing_score = display_wellbeing_score(latest_entry)
    
    with col2:
        # Display summary of responses
        st.markdown("### Based on your responses:")
        
        # Show different metrics
        metrics_col1, metrics_col2 = st.columns(2)
        
        with metrics_col1:
            mood_mapping = {
                1: "Struggling 😢", 
                2: "Low 😔", 
                3: "Neutral 😐", 
                4: "Good 🙂", 
                5: "Great 😄"
            }
            mood_text = mood_mapping.get(latest_entry.get("mood", 3), "Not specified")
            st.metric("Mood", mood_text)
            
            if "anxiety" in latest_entry:
                anxiety_status = "Yes 😰" if latest_entry["anxiety"] else "No 😌"
                st.metric("Feeling Anxious", anxiety_status)
        
        with metrics_col2:
            if "sleep" in latest_entry:
                sleep_text = f"{latest_entry['sleep']}/5 😴"
                st.metric("Sleep Quality", sleep_text)
            
            if "stress" in latest_entry:
                stress_text = f"{latest_entry['stress']}/5 😬"
                st.metric("Stress Level", stress_text)
        
        # Show platform-specific data if available
        if "platform" in latest_entry:
            st.markdown(f"#### {latest_entry['platform']} Usage:")
            if "platform_time" in latest_entry:
                st.write(f"Time spent: {latest_entry['platform_time']}")
            if "content_impact" in latest_entry:
                impact = latest_entry['content_impact']
                emoji = "😊" if impact == "Positive" else "😐" if impact == "Neutral" else "😔"
                st.write(f"Impact on mood: {impact} {emoji}")
    
    # Middle section: AI Tips
    st.markdown("---")
    st.subheader("Personalized Suggestions For You")
    
    # Generate or retrieve suggestions
    if "ai_suggestions" not in st.session_state or not st.session_state["ai_suggestions"]:
        with st.spinner("Generating personalized suggestions..."):
            platform = latest_entry.get("platform", None)
            suggestions = generate_wellness_suggestions(latest_entry, platform)
            st.session_state["ai_suggestions"] = suggestions
    else:
        suggestions = st.session_state["ai_suggestions"]
    
    # Display suggestions in cards
    if len(suggestions) > 0:
        # Distribute suggestions evenly in columns
        cols = st.columns(min(3, len(suggestions)))
        for i, suggestion in enumerate(suggestions):
            with cols[i % len(cols)]:
                st.markdown(f"""
                <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px; margin-bottom: 10px; height: 100%;">
                    <h3>{suggestion.get('emoji', '✨')} {suggestion.get('title', 'Suggestion')}</h3>
                    <p>{suggestion.get('description', '')}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No suggestions available. Try completing a new assessment.")
    
    # Bottom section: Motivation
    st.markdown("---")
    st.subheader("You Are Not Alone")
    
    st.markdown("""
    Remember that managing your digital wellbeing is a journey. Small, consistent changes 
    often lead to the most significant improvements in mental health. Be patient with yourself
    and celebrate the steps you take, no matter how small they may seem.
    """)
    
    # Actions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Get New Suggestions", key="refresh_suggestions"):
            # Clear existing suggestions to generate new ones
            st.session_state["ai_suggestions"] = []
            st.rerun()
    
    with col2:
        if st.button("Track My Progress", key="view_progress"):
            st.switch_page("pages/3_Progress_Tracker.py")
    
    with col3:
        if st.button("Take Another Assessment", key="new_assessment"):
            st.session_state["current_step"] = 1
            st.session_state["current_responses"] = {}
            st.switch_page("pages/1_Questionnaire.py")

if __name__ == "__main__":
    main()
