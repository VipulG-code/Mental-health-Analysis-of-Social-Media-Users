import streamlit as st
from utils.data_utils import initialize_session_state

# Page configuration
st.set_page_config(
    page_title="About | Mental Wellness Tracker",
    page_icon="🌱",
    layout="wide"
)

# Initialize session state
initialize_session_state()

def main():
    st.markdown("<h1 style='text-align: center;'>About Mental Wellness Tracker</h1>", unsafe_allow_html=True)
    
    # Top section: Mission statement
    st.subheader("Why We Built This")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Our Mission
        
        The Mental Wellness Tracker was created with a simple mission: to help people understand 
        and improve their mental wellbeing in the digital age.
        
        In a world where we spend increasing amounts of time on social media and digital platforms, 
        it's important to be aware of how these interactions affect our mental health. Our tool helps you:
        
        - **Track your mood** and mental state over time
        - **Identify patterns** between platform usage and emotional wellbeing
        - **Receive personalized suggestions** for improving digital wellness
        - **Visualize progress** on your mental health journey
        
        We believe that awareness is the first step toward positive change. By regularly checking in 
        with yourself and tracking your mental wellness, you can make informed decisions about your 
        digital habits and take control of your online experiences.
        """)
    
    with col2:
        st.markdown("""
        <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px; text-align: center;">
            <h3>💭 Did You Know?</h3>
            <p>Studies show that the average person spends over 2 hours per day on social media platforms.</p>
            <p>Even small changes in how we use these platforms can have significant impacts on mental wellbeing.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Middle section: How it works
    st.markdown("---")
    st.subheader("How It Works")
    
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin: 20px 0;">
        <div style="text-align: center; flex: 1;">
            <div style="background-color: #6C5CE7; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin: 0 auto;">1</div>
            <h4>Take the Assessment</h4>
            <p>Answer questions about your mood, stress, and platform usage</p>
        </div>
        <div style="text-align: center; flex: 1;">
            <div style="background-color: #6C5CE7; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin: 0 auto;">2</div>
            <h4>Get AI Suggestions</h4>
            <p>Receive personalized tips based on your responses</p>
        </div>
        <div style="text-align: center; flex: 1;">
            <div style="background-color: #6C5CE7; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin: 0 auto;">3</div>
            <h4>Track Progress</h4>
            <p>Visualize your mental wellness journey over time</p>
        </div>
        <div style="text-align: center; flex: 1;">
            <div style="background-color: #6C5CE7; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin: 0 auto;">4</div>
            <h4>Make Changes</h4>
            <p>Implement suggestions and re-evaluate regularly</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Privacy & Data Security
    
    Your mental health data is important and sensitive. That's why:
    
    - All your data is stored locally in your browser's session
    - We don't share your responses with third parties
    - No personal identifying information is required
    - Data is used only to provide personalized suggestions
    
    You're in control of your data and your journey.
    """)
    
    # Bottom section: FAQ and Help
    st.markdown("---")
    st.subheader("Frequently Asked Questions")
    
    # FAQ Expanders
    with st.expander("How often should I take the assessment?"):
        st.write("""
        We recommend taking the assessment regularly - once a week is ideal for most people. 
        However, if you're going through a particularly challenging time or making active changes 
        to your digital habits, you might benefit from checking in more frequently.
        
        Remember, consistency is more important than frequency. Find a schedule that works for you 
        and that you can maintain over time.
        """)
    
    with st.expander("Is my data saved between sessions?"):
        st.write("""
        Your data is stored in your browser's session storage, which means it will persist as long 
        as you keep the browser tab open or until you clear your browser data.
        
        In future versions, we plan to add optional user accounts for those who want to save their 
        progress long-term.
        """)
    
    with st.expander("How are the AI suggestions generated?"):
        st.write("""
        The AI suggestions are generated using OpenAI's GPT model, which analyzes your responses 
        to the assessment questions and identifies patterns and potential areas for improvement.
        
        The suggestions are personalized based on:
        - Your current mood and stress levels
        - Sleep quality and anxiety indicators
        - Platform-specific usage patterns (if provided)
        - Historical trends in your data (for returning users)
        
        The AI is designed to provide practical, actionable advice rather than generic wellness tips.
        """)
    
    with st.expander("Can I use this tool if I'm experiencing a mental health crisis?"):
        st.write("""
        This tool is designed for general wellness tracking and is not a substitute for professional 
        mental health care. If you're experiencing a crisis or severe mental health symptoms, please 
        contact a mental health professional or crisis hotline immediately.
        
        **Resources for immediate help:**
        - National Suicide Prevention Lifeline: 1-800-273-8255
        - Crisis Text Line: Text HOME to 741741
        - International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/
        """)
    
    # Contact section
    st.markdown("---")
    st.subheader("Get in Touch")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Have Questions or Feedback?
        
        We'd love to hear from you! Your feedback helps us improve the Mental Wellness Tracker.
        
        - 📧 Email: support@mentalwellnesstracker.com
        - 🐦 Twitter: @MentalWellnessT
        - 📱 Instagram: @MentalWellnessTracker
        """)
    
    with col2:
        st.markdown("""
        ### Report an Issue
        
        Found a bug or having technical difficulties? Let us know by filling out our issue report form.
        """)
        
        issue_type = st.selectbox("Type of issue", ["Select issue type", "Bug report", "Feature request", "Data concern", "Other"])
        issue_description = st.text_area("Description", height=100, placeholder="Please describe the issue in detail...")
        
        if st.button("Submit Issue"):
            if issue_type != "Select issue type" and issue_description:
                st.success("Thank you for your report! We'll look into this issue promptly.")
            else:
                st.error("Please select an issue type and provide a description.")

if __name__ == "__main__":
    main()
