import streamlit as st
import datetime
from utils.data_utils import initialize_session_state, save_user_data
from utils.ui_utils import display_progress_bar

# Page configuration
st.set_page_config(
    page_title="Mental Health Check | Mental Wellness Tracker",
    page_icon="🌱",
    layout="wide"
)

# Initialize session state
initialize_session_state()

# Main function
def main():
    st.markdown("<h1 style='text-align: center;'>Daily Mental Health Check</h1>", unsafe_allow_html=True)
    st.write("Let's take a moment to reflect on how you're feeling today")
    
    # Initialize or get the current step
    current_step = st.session_state.get("current_step", 1)
    total_steps = 4
    
    # Display progress bar
    display_progress_bar(current_step, total_steps)
    
    # Platform-specific text
    platform = st.session_state.get("selected_platform", None)
    platform_text = f" for {platform}" if platform else ""
    
    # Step 1: General Mood Check
    if current_step == 1:
        st.subheader(f"Step {current_step} of {total_steps}: General Mood Check{platform_text}")
        
        # Question 1: Mood
        st.markdown("### How are you *really* feeling today?")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("😄", key="mood_5", help="Great"):
                st.session_state["current_responses"]["mood"] = 5
                st.session_state["current_step"] = 2
                st.rerun()
        with col2:
            if st.button("🙂", key="mood_4", help="Good"):
                st.session_state["current_responses"]["mood"] = 4
                st.session_state["current_step"] = 2
                st.rerun()
        with col3:
            if st.button("😐", key="mood_3", help="Neutral"):
                st.session_state["current_responses"]["mood"] = 3
                st.session_state["current_step"] = 2
                st.rerun()
        with col4:
            if st.button("😔", key="mood_2", help="Low"):
                st.session_state["current_responses"]["mood"] = 2
                st.session_state["current_step"] = 2
                st.rerun()
        with col5:
            if st.button("😢", key="mood_1", help="Struggling"):
                st.session_state["current_responses"]["mood"] = 1
                st.session_state["current_step"] = 2
                st.rerun()
    
    # Step 2: Sleep Quality
    elif current_step == 2:
        st.subheader(f"Step {current_step} of {total_steps}: Sleep & Rest{platform_text}")
        
        # Question: Sleep quality
        st.markdown("### How was your sleep?")
        sleep_value = st.slider(
            "Drag the slider", 
            min_value=1, 
            max_value=5,
            value=3,
            step=1,
            help="1 = Poor sleep, 5 = Great sleep",
            label_visibility="collapsed"
        )
        st.session_state["current_responses"]["sleep"] = sleep_value
        
        # Button to continue
        if st.button("Continue to next question", key="sleep_continue"):
            st.session_state["current_step"] = 3
            st.rerun()
    
    # Step 3: Stress & Anxiety
    elif current_step == 3:
        st.subheader(f"Step {current_step} of {total_steps}: Stress & Anxiety{platform_text}")
        
        # Question: Stress level
        st.markdown("### What's your stress level today?")
        stress_value = st.slider(
            "Drag the slider", 
            min_value=1, 
            max_value=5, 
            value=3,
            step=1,
            help="1 = Very low stress, 5 = Very high stress",
            label_visibility="collapsed"
        )
        st.session_state["current_responses"]["stress"] = stress_value
        
        # Question: Anxiety
        st.markdown("### Did you feel anxious today?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("No", key="anxiety_no", use_container_width=True):
                st.session_state["current_responses"]["anxiety"] = False
                st.session_state["current_step"] = 4
                st.rerun()
        with col2:
            if st.button("Yes", key="anxiety_yes", use_container_width=True):
                st.session_state["current_responses"]["anxiety"] = True
                st.session_state["current_step"] = 4
                st.rerun()
    
    # Step 4: Platform-specific questions (if a platform is selected)
    elif current_step == 4:
        platform = st.session_state.get("selected_platform", None)
        if platform:
            st.subheader(f"Step {current_step} of {total_steps}: {platform} Impact")
            
            # Screen time
            st.markdown(f"### How much time did you spend on {platform} today?")
            time_options = ["Less than 30 minutes", "30 minutes to 1 hour", 
                          "1-2 hours", "2-3 hours", "More than 3 hours"]
            selected_time = st.select_slider(
                "Select time range",
                options=time_options,
                value="1-2 hours",
                label_visibility="collapsed"
            )
            st.session_state["current_responses"]["platform_time"] = selected_time
            
            # Content impact
            st.markdown(f"### How did content on {platform} make you feel today?")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("😊 Positive", key="content_positive", use_container_width=True):
                    st.session_state["current_responses"]["content_impact"] = "Positive"
                    st.session_state["current_responses"]["platform"] = platform
                    save_and_redirect()
            with col2:
                if st.button("😐 Neutral", key="content_neutral", use_container_width=True):
                    st.session_state["current_responses"]["content_impact"] = "Neutral"
                    st.session_state["current_responses"]["platform"] = platform
                    save_and_redirect()
            with col3:
                if st.button("😔 Negative", key="content_negative", use_container_width=True):
                    st.session_state["current_responses"]["content_impact"] = "Negative"
                    st.session_state["current_responses"]["platform"] = platform
                    save_and_redirect()
        else:
            # Final submission without platform-specific questions
            st.subheader(f"Step {current_step} of {total_steps}: Final Thoughts")
            
            st.markdown("### Any additional notes about your day?")
            notes = st.text_area("Optional: Share any thoughts, triggers, or positive moments", 
                                height=100, max_chars=500, placeholder="Type here...")
            
            st.session_state["current_responses"]["notes"] = notes
            
            if st.button("Submit", type="primary"):
                save_and_redirect()
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if current_step > 1:
            if st.button("← Back", key="back_button"):
                st.session_state["current_step"] = current_step - 1
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.caption("Your responses are stored securely and used only to provide personalized wellness suggestions.")

def save_and_redirect():
    """Save the current responses and redirect to AI suggestions page"""
    save_user_data(st.session_state["current_responses"])
    st.session_state["selected_platform"] = None
    st.switch_page("pages/2_AI_Suggestions.py")

if __name__ == "__main__":
    main()
