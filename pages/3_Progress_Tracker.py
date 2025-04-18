import streamlit as st
import pandas as pd
import altair as alt
from utils.data_utils import initialize_session_state, get_mood_data_as_df, calculate_wellbeing_score

# Page configuration
st.set_page_config(
    page_title="Progress Tracker | Mental Wellness Tracker",
    page_icon="🌱",
    layout="wide"
)

# Initialize session state
initialize_session_state()

def main():
    st.markdown("<h1 style='text-align: center;'>Progress Tracker</h1>", unsafe_allow_html=True)
    st.write("Here's your mental wellness journey over time")
    
    # Check if we have enough mood data
    if not st.session_state.get("mood_data", []) or len(st.session_state["mood_data"]) < 1:
        st.warning("You need to complete at least one assessment to track progress.")
        if st.button("Go to Questionnaire"):
            st.switch_page("pages/1_Questionnaire.py")
        return
    
    # Get mood data as DataFrame
    df = get_mood_data_as_df()
    
    # Calculate wellbeing scores for each entry
    if not df.empty:
        df['wellbeing_score'] = df.apply(calculate_wellbeing_score, axis=1)
    
    # Top section: Charts
    st.subheader("📊 Your Progress Over Time")
    
    if len(df) >= 2:
        # Multiple data points: show line chart
        tab1, tab2, tab3 = st.tabs(["Wellbeing Score", "Mood & Sleep", "Stress & Anxiety"])
        
        with tab1:
            # Wellbeing score chart
            wellbeing_chart = alt.Chart(df).mark_line(point=True).encode(
                x=alt.X('date:T', title='Date'),
                y=alt.Y('wellbeing_score:Q', title='Wellbeing Score', scale=alt.Scale(domain=[0, 100])),
                tooltip=['date:T', 'wellbeing_score:Q']
            ).properties(
                title='Wellbeing Score Trend',
                height=300
            ).interactive()
            
            st.altair_chart(wellbeing_chart, use_container_width=True)
            
            # Calculate improvement
            first_score = df.iloc[0]['wellbeing_score']
            last_score = df.iloc[-1]['wellbeing_score']
            improvement = last_score - first_score
            improvement_percent = (improvement / first_score * 100) if first_score > 0 else 0
            
            if improvement > 0:
                st.success(f"Your wellbeing score has improved by {improvement_percent:.1f}% since you started!")
            elif improvement < 0:
                st.info(f"Your wellbeing score has decreased by {abs(improvement_percent):.1f}%. Remember, progress isn't always linear.")
            else:
                st.info("Your wellbeing score has remained stable.")
            
        with tab2:
            # Mood and sleep chart
            if 'mood' in df.columns and 'sleep' in df.columns:
                mood_sleep_df = df[['date', 'mood', 'sleep']].copy()
                # Reshape for Altair
                mood_sleep_df = pd.melt(mood_sleep_df, id_vars=['date'], value_vars=['mood', 'sleep'])
                
                mood_sleep_chart = alt.Chart(mood_sleep_df).mark_line(point=True).encode(
                    x=alt.X('date:T', title='Date'),
                    y=alt.Y('value:Q', title='Rating (1-5)'),
                    color=alt.Color('variable:N', title='Metric', 
                                    scale=alt.Scale(domain=['mood', 'sleep'], 
                                                    range=['#6C5CE7', '#00b894'])),
                    tooltip=['date:T', 'variable:N', 'value:Q']
                ).properties(
                    title='Mood & Sleep Quality',
                    height=300
                ).interactive()
                
                st.altair_chart(mood_sleep_chart, use_container_width=True)
            else:
                st.info("Mood and sleep data not available for all entries.")
            
        with tab3:
            # Stress and anxiety chart
            if 'stress' in df.columns and 'anxiety' in df.columns:
                # Convert boolean anxiety to numeric
                df['anxiety_numeric'] = df['anxiety'].apply(lambda x: 1 if x else 0)
                stress_anxiety_df = df[['date', 'stress', 'anxiety_numeric']].copy()
                stress_anxiety_df = pd.melt(stress_anxiety_df, id_vars=['date'], 
                                         value_vars=['stress', 'anxiety_numeric'])
                
                # Rename for better labels
                stress_anxiety_df['variable'] = stress_anxiety_df['variable'].replace({
                    'stress': 'Stress Level', 
                    'anxiety_numeric': 'Anxiety Present'
                })
                
                stress_chart = alt.Chart(stress_anxiety_df[stress_anxiety_df['variable'] == 'Stress Level']).mark_line(point=True).encode(
                    x=alt.X('date:T', title='Date'),
                    y=alt.Y('value:Q', title='Rating (1-5)'),
                    color=alt.value('#e74c3c'),
                    tooltip=['date:T', 'value:Q']
                ).properties(
                    title='Stress Level Trend',
                    height=300
                ).interactive()
                
                anxiety_chart = alt.Chart(stress_anxiety_df[stress_anxiety_df['variable'] == 'Anxiety Present']).mark_bar().encode(
                    x=alt.X('date:T', title='Date'),
                    y=alt.Y('value:Q', title='Anxiety (0=No, 1=Yes)'),
                    color=alt.value('#f39c12'),
                    tooltip=['date:T', 'value:Q']
                ).properties(
                    title='Anxiety Occurrences',
                    height=150
                ).interactive()
                
                st.altair_chart(stress_chart, use_container_width=True)
                st.altair_chart(anxiety_chart, use_container_width=True)
            else:
                st.info("Stress and anxiety data not available for all entries.")
    
    else:
        # Single data point: show metrics
        st.info("Complete more assessments to see your progress over time.")
        
        # Show current metrics
        entry = df.iloc[0].to_dict()
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Wellbeing Score", f"{int(entry.get('wellbeing_score', 0))}/100")
        
        with col2:
            mood_value = entry.get('mood', 'N/A')
            mood_label = {1: "Struggling", 2: "Low", 3: "Neutral", 4: "Good", 5: "Great"}.get(mood_value, "N/A")
            st.metric("Mood", f"{mood_label} ({mood_value}/5)")
        
        with col3:
            sleep_value = entry.get('sleep', 'N/A')
            st.metric("Sleep Quality", f"{sleep_value}/5")
        
        with col4:
            stress_value = entry.get('stress', 'N/A')
            st.metric("Stress Level", f"{stress_value}/5")
    
    # Middle section: Badges and achievements
    st.markdown("---")
    st.subheader("🏆 Your Achievements")
    
    # Calculate badges
    num_entries = len(df)
    
    # Create badge cards
    cols = st.columns(3)
    
    with cols[0]:
        if num_entries >= 1:
            st.markdown("""
            <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px; text-align: center;">
                <h3>🚀 First Check-in</h3>
                <p>You've taken the first step on your wellness journey!</p>
            </div>
            """, unsafe_allow_html=True)
    
    with cols[1]:
        if num_entries >= 3:
            st.markdown("""
            <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px; text-align: center;">
                <h3>🔍 Self-Awareness</h3>
                <p>Completed 3+ mental wellness checks</p>
            </div>
            """, unsafe_allow_html=True)
        elif num_entries >= 1:
            st.markdown("""
            <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px; text-align: center; opacity: 0.5;">
                <h3>🔍 Self-Awareness</h3>
                <p>Complete 3+ mental wellness checks</p>
                <p><small>Progress: {}/{}</small></p>
            </div>
            """.format(num_entries, 3), unsafe_allow_html=True)
    
    with cols[2]:
        # Check if wellbeing score improved
        if num_entries >= 2 and df.iloc[-1]['wellbeing_score'] > df.iloc[0]['wellbeing_score']:
            st.markdown("""
            <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px; text-align: center;">
                <h3>📈 Progress Maker</h3>
                <p>Improved your wellbeing score!</p>
            </div>
            """, unsafe_allow_html=True)
        elif num_entries >= 2:
            st.markdown("""
            <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px; text-align: center; opacity: 0.5;">
                <h3>📈 Progress Maker</h3>
                <p>Improve your wellbeing score</p>
                <p><small>Keep working toward improvement</small></p>
            </div>
            """, unsafe_allow_html=True)
    
    # Bottom section: Feedback
    st.markdown("---")
    st.subheader("💭 Reflection")
    
    st.write("What has helped you most on your mental wellness journey?")
    
    feedback_options = [
        "Regular check-ins & self-awareness",
        "AI suggestions & tips",
        "Tracking progress over time",
        "Setting digital wellbeing boundaries",
        "Something else"
    ]
    
    selected_feedback = st.multiselect("Select all that apply", options=feedback_options)
    
    if "Something else" in selected_feedback:
        other_feedback = st.text_area("Please share what's helped you", height=100)
    
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback! Your insights help us improve.")
    
    # Actions
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Take Another Assessment", key="new_assessment"):
            st.session_state["current_step"] = 1
            st.session_state["current_responses"] = {}
            st.switch_page("pages/1_Questionnaire.py")
    
    with col2:
        if st.button("View AI Suggestions", key="view_suggestions"):
            st.switch_page("pages/2_AI_Suggestions.py")

if __name__ == "__main__":
    main()
