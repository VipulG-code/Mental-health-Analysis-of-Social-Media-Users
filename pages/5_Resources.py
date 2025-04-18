import streamlit as st
import random
from assets.quotes import motivational_quotes
from utils.data_utils import initialize_session_state, get_random_quote

# Page configuration
st.set_page_config(
    page_title="Resources | Mental Wellness Tracker",
    page_icon="🌱",
    layout="wide"
)

# Initialize session state
initialize_session_state()

def main():
    st.markdown("<h1 style='text-align: center;'>Motivation & Resources</h1>", unsafe_allow_html=True)
    
    # Top section: Daily motivation
    st.subheader("✨ Daily Inspiration")
    
    # Display 3 random quotes in a carousel-like layout
    quote_indices = random.sample(range(len(motivational_quotes)), min(3, len(motivational_quotes)))
    
    cols = st.columns(3)
    for i, idx in enumerate(quote_indices):
        quote = motivational_quotes[idx]
        with cols[i]:
            st.markdown(f"""
            <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px; height: 100%; text-align: center;">
                <p style="font-style: italic;">"{quote['quote']}"</p>
                <p>— {quote['author']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Middle section: Helpful resources
    st.markdown("---")
    st.subheader("📚 Helpful Resources")
    
    # Create tabs for different types of resources
    tab1, tab2, tab3 = st.tabs(["Articles & Guides", "Videos", "Apps & Tools"])
    
    with tab1:
        st.markdown("### Articles on Digital Wellbeing")
        
        article1, article2 = st.columns(2)
        
        with article1:
            st.markdown("""
            <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                <h4>How Social Media Affects Mental Health</h4>
                <p>Learn about the psychological impact of excessive social media usage and strategies to create healthier digital habits.</p>
                <p><a href="https://www.helpguide.org/articles/mental-health/social-media-and-mental-health.htm" target="_blank">Read on HelpGuide.org →</a></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px;">
                <h4>Setting Digital Boundaries</h4>
                <p>Practical tips for creating healthy boundaries with technology and reclaiming your time and attention.</p>
                <p><a href="https://www.mindful.org/how-to-create-tech-life-balance/" target="_blank">Read on Mindful.org →</a></p>
            </div>
            """, unsafe_allow_html=True)
        
        with article2:
            st.markdown("""
            <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                <h4>Mindfulness for Digital Distraction</h4>
                <p>Learn mindfulness techniques specifically designed to help manage the constant pull of digital notifications.</p>
                <p><a href="https://www.verywellmind.com/mindfulness-exercises-for-everyday-life-3145187" target="_blank">Read on VeryWellMind →</a></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px;">
                <h4>FOMO and Social Media Anxiety</h4>
                <p>Understanding the fear of missing out and strategies to overcome social comparison on platforms.</p>
                <p><a href="https://www.psychologytoday.com/us/blog/the-upside-things/202109/how-stop-fomo-and-social-media-anxiety" target="_blank">Read on Psychology Today →</a></p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Helpful Videos")
        
        video1, video2 = st.columns(2)
        
        with video1:
            st.markdown("""
            <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                <h4>Digital Minimalism: Cal Newport</h4>
                <iframe width="100%" height="200" src="https://www.youtube.com/embed/3E7hkPZ-HTk" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                <p>Learn about the concept of digital minimalism and how to be more intentional with technology.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with video2:
            st.markdown("""
            <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                <h4>How to Break Your Social Media Addiction</h4>
                <iframe width="100%" height="200" src="https://www.youtube.com/embed/3GM8CKlmsp8" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                <p>Practical steps to reduce dependency on social media platforms and reclaim your focus.</p>
            </div>
            """, unsafe_allow_html=True)
        
        video3, video4 = st.columns(2)
        
        with video3:
            st.markdown("""
            <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px;">
                <h4>5-Minute Mindfulness Meditation</h4>
                <iframe width="100%" height="200" src="https://www.youtube.com/embed/inpok4MKVLM" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                <p>A quick mindfulness exercise you can do any time you feel overwhelmed by digital stimuli.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with video4:
            st.markdown("""
            <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px;">
                <h4>The Social Dilemma: Insights</h4>
                <iframe width="100%" height="200" src="https://www.youtube.com/embed/uaaC57tcci0" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                <p>Key insights from the documentary about social media's impact on our lives and mental health.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Apps & Tools for Digital Wellbeing")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px; height: 100%;">
                <h4>Forest App</h4>
                <p>Stay focused and present by planting virtual trees that grow while you're away from your phone.</p>
                <p><a href="https://www.forestapp.cc/" target="_blank">Learn More →</a></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px; height: 100%;">
                <h4>Headspace</h4>
                <p>Guided meditation and mindfulness exercises to help reduce stress and improve focus.</p>
                <p><a href="https://www.headspace.com/" target="_blank">Learn More →</a></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px; height: 100%;">
                <h4>Freedom</h4>
                <p>Block distracting websites and apps to help you stay focused and mindful of your digital usage.</p>
                <p><a href="https://freedom.to/" target="_blank">Learn More →</a></p>
            </div>
            """, unsafe_allow_html=True)
        
        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.markdown("""
            <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px; height: 100%;">
                <h4>Calm</h4>
                <p>Sleep stories, meditation guides, and relaxing music to help reduce anxiety and improve sleep.</p>
                <p><a href="https://www.calm.com/" target="_blank">Learn More →</a></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown("""
            <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px; height: 100%;">
                <h4>Moment</h4>
                <p>Track your phone usage and set daily limits to become more aware of your digital habits.</p>
                <p><a href="https://inthemoment.io/" target="_blank">Learn More →</a></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col6:
            st.markdown("""
            <div style="background-color: #f0f2f6; border-radius: 10px; padding: 15px; height: 100%;">
                <h4>Insight Timer</h4>
                <p>Free meditation app with thousands of guided sessions for stress, anxiety, and better sleep.</p>
                <p><a href="https://insighttimer.com/" target="_blank">Learn More →</a></p>
            </div>
            """, unsafe_allow_html=True)
    
    # Bottom section: Self-care tracker
    st.markdown("---")
    st.subheader("📝 Daily Self-Care Checklist")
    
    st.write("Track your daily self-care activities to maintain your mental wellbeing:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Drank enough water today", key="water_check")
        st.checkbox("Took deep breaths when stressed", key="breathing_check")
        st.checkbox("Got enough sleep (7-8 hours)", key="sleep_check")
        st.checkbox("Took breaks from screens", key="screen_break_check")
    
    with col2:
        st.checkbox("Spent time in nature", key="nature_check")
        st.checkbox("Connected with a loved one", key="connection_check")
        st.checkbox("Limited social media usage", key="social_media_check")
        st.checkbox("Did something I enjoy", key="enjoyment_check")
    
    if st.button("Save Today's Self-Care Checklist"):
        # Count checked items
        checked_items = sum([
            st.session_state.get("water_check", False),
            st.session_state.get("breathing_check", False),
            st.session_state.get("sleep_check", False),
            st.session_state.get("screen_break_check", False),
            st.session_state.get("nature_check", False),
            st.session_state.get("connection_check", False),
            st.session_state.get("social_media_check", False),
            st.session_state.get("enjoyment_check", False)
        ])
        
        if checked_items >= 6:
            st.success(f"Great job! You completed {checked_items}/8 self-care activities today.")
        elif checked_items >= 3:
            st.info(f"You're on your way! You completed {checked_items}/8 self-care activities today.")
        else:
            st.warning(f"You completed {checked_items}/8 self-care activities. Remember, small steps count!")

if __name__ == "__main__":
    main()
