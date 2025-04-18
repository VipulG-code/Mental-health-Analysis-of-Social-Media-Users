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

# Instagram Questionnaire
instagram_questions = [
    {
        "id": "instagram_experience",
        "text": "How would you describe your current experience with Instagram?",
        "options": [
            "Uplifting and inspiring",
            "A mix of fun and distraction",
            "Sometimes overwhelming",
            "I'd like to explore a healthier balance"
        ]
    },
    {
        "id": "instagram_frequency",
        "text": "How often do you use Instagram during your free time?",
        "options": [
            "Rarely",
            "Occasionally",
            "A few times a day",
            "Regularly throughout the day"
        ]
    },
    {
        "id": "instagram_content",
        "text": "What type of content do you engage with the most?",
        "options": [
            "Educational and career-oriented",
            "Fitness, motivation, or self-growth",
            "Entertainment and lifestyle",
            "Mixed or not sure"
        ]
    },
    {
        "id": "instagram_feeling",
        "text": "After using Instagram, how do you typically feel?",
        "options": [
            "Energized and positive",
            "Neutral",
            "Slightly distracted",
            "Emotionally drained or overstimulated"
        ]
    },
    {
        "id": "instagram_self_image",
        "text": "Has Instagram influenced your self-image or emotions?",
        "options": [
            "Not really",
            "Sometimes I feel inspired, other times unsure",
            "Yes, I've reflected more on how I view myself",
            "Yes, and I'm looking to understand this better"
        ]
    },
    {
        "id": "instagram_growth",
        "text": "Does Instagram help or hinder your personal growth?",
        "options": [
            "It supports my goals",
            "A bit of both",
            "It distracts me at times",
            "I'd like to realign my time better"
        ]
    },
    {
        "id": "instagram_engagement",
        "text": "How important are likes/comments/followers to you?",
        "options": [
            "Not important",
            "Somewhat noticeable",
            "I often track them",
            "I feel affected when engagement changes"
        ]
    },
    {
        "id": "instagram_boundaries",
        "text": "Would you consider taking breaks or setting boundaries with Instagram?",
        "options": [
            "I already take breaks regularly",
            "I've considered it but haven't started",
            "It's hard to step away",
            "I'd like help creating healthy boundaries"
        ]
    },
    {
        "id": "instagram_resources",
        "text": "Would you be interested in resources or support for mindful Instagram use?",
        "options": [
            "Yes, that would be helpful",
            "Maybe, if it fits my needs",
            "Not right now",
            "I'm not sure"
        ]
    }
]

# Facebook Questionnaire
facebook_questions = [
    {
        "id": "facebook_frequency",
        "text": "How often do you check Facebook?",
        "options": [
            "Occasionally",
            "Once or twice daily",
            "Several times a day",
            "Continuously throughout the day"
        ]
    },
    {
        "id": "facebook_purpose",
        "text": "What do you mainly use Facebook for?",
        "options": [
            "Staying in touch with friends/family",
            "Sharing memories or thoughts",
            "Browsing groups or marketplace",
            "A mix of everything"
        ]
    },
    {
        "id": "facebook_feeling",
        "text": "How do you usually feel after using Facebook?",
        "options": [
            "Connected and positive",
            "Neutral",
            "Slightly distracted or overwhelmed",
            "Anxious or left out"
        ]
    },
    {
        "id": "facebook_comparison",
        "text": "Do you find yourself comparing your life with others based on posts?",
        "options": [
            "Not at all",
            "Occasionally",
            "Frequently",
            "Almost always"
        ]
    },
    {
        "id": "facebook_meaningful",
        "text": "How often do you feel your time on Facebook is meaningful?",
        "options": [
            "Very often",
            "Sometimes",
            "Rarely",
            "Unsure"
        ]
    },
    {
        "id": "facebook_interactions",
        "text": "Do interactions (likes, comments) influence how you feel about yourself or others?",
        "options": [
            "Not really",
            "Occasionally",
            "Yes, sometimes",
            "Yes, frequently"
        ]
    },
    {
        "id": "facebook_emotional",
        "text": "Do family posts or social updates ever trigger emotional reactions?",
        "options": [
            "Not at all",
            "Slightly",
            "Often",
            "Strongly"
        ]
    },
    {
        "id": "facebook_goals",
        "text": "Does Facebook support or distract you from personal goals or mental peace?",
        "options": [
            "It supports me",
            "A mix of both",
            "It distracts me occasionally",
            "It affects me deeply"
        ]
    },
    {
        "id": "facebook_communities",
        "text": "Do you use Facebook groups or communities for emotional support or hobbies?",
        "options": [
            "Yes, regularly",
            "Sometimes",
            "Rarely",
            "No"
        ]
    },
    {
        "id": "facebook_tips",
        "text": "Are you open to mental wellness tips tailored to your Facebook use?",
        "options": [
            "Yes",
            "Maybe",
            "Not sure",
            "No"
        ]
    }
]

# Snapchat Questionnaire
snapchat_questions = [
    {
        "id": "snapchat_frequency",
        "text": "How often do you use Snapchat daily?",
        "options": [
            "Less than 30 minutes",
            "30 minutes to 1 hour",
            "1–2 hours",
            "More than 2 hours"
        ]
    },
    {
        "id": "snapchat_purpose",
        "text": "What do you primarily use Snapchat for?",
        "options": [
            "Staying connected with friends",
            "Sharing personal moments",
            "Exploring content/stories",
            "Maintaining streaks"
        ]
    },
    {
        "id": "snapchat_streaks",
        "text": "How do you feel when a streak breaks or snaps go unanswered?",
        "options": [
            "Unaffected",
            "Slightly concerned",
            "Stressed or anxious",
            "Upset or emotional"
        ]
    },
    {
        "id": "snapchat_fomo",
        "text": "Do you ever feel left out due to content shared by others?",
        "options": [
            "Never",
            "Rarely",
            "Sometimes",
            "Often"
        ]
    },
    {
        "id": "snapchat_image",
        "text": "How much effort do you put into appearing fun or perfect on Snapchat?",
        "options": [
            "None — I post casually",
            "A little — for fun",
            "Moderate — I like to be seen a certain way",
            "A lot — I feel pressured to present a certain image"
        ]
    },
    {
        "id": "snapchat_connection",
        "text": "Do you feel seen and understood through your Snapchat interactions?",
        "options": [
            "Yes, always",
            "Mostly",
            "Sometimes",
            "Rarely"
        ]
    },
    {
        "id": "snapchat_emotional",
        "text": "How does using Snapchat affect your emotional state overall?",
        "options": [
            "I feel happy and connected",
            "Neutral",
            "Mixed emotions",
            "Emotionally drained sometimes"
        ]
    },
    {
        "id": "snapchat_impact",
        "text": "Has your Snapchat use ever impacted your studies, work, or goals?",
        "options": [
            "Never",
            "Rarely",
            "Occasionally",
            "Often"
        ]
    },
    {
        "id": "snapchat_authenticity",
        "text": "Do you feel comfortable expressing your real self on Snapchat?",
        "options": [
            "Always",
            "Mostly",
            "Sometimes",
            "Not really"
        ]
    },
    {
        "id": "snapchat_balance",
        "text": "Would you like tips to better balance your digital and emotional life?",
        "options": [
            "Definitely",
            "Maybe",
            "Not sure",
            "No"
        ]
    }
]

# Twitter Questionnaire
twitter_questions = [
    {
        "id": "twitter_experience",
        "text": "How would you describe your experience with Twitter/X?",
        "options": [
            "Engaging and informative",
            "A mix of value and noise",
            "Sometimes intense or draining",
            "I use it mostly out of habit"
        ]
    },
    {
        "id": "twitter_content",
        "text": "What kind of content do you usually interact with?",
        "options": [
            "News and world events",
            "Memes and humor",
            "Discussions and debates",
            "A variety / not sure"
        ]
    },
    {
        "id": "twitter_feeling",
        "text": "After scrolling through Twitter, how do you typically feel?",
        "options": [
            "Informed and curious",
            "Neutral or unaffected",
            "A bit overwhelmed or reactive",
            "Emotionally unsettled"
        ]
    },
    {
        "id": "twitter_trending",
        "text": "How frequently do trending topics affect your emotions or opinions?",
        "options": [
            "Rarely",
            "Sometimes",
            "Frequently",
            "Very often"
        ]
    },
    {
        "id": "twitter_arguments",
        "text": "Do online arguments or intense threads impact your mood?",
        "options": [
            "Not at all",
            "Occasionally",
            "Yes, they sometimes affect me",
            "Yes, quite significantly"
        ]
    },
    {
        "id": "twitter_expression",
        "text": "Do you use Twitter to express emotions or vent?",
        "options": [
            "Never",
            "Rarely",
            "Sometimes",
            "Frequently"
        ]
    },
    {
        "id": "twitter_pressure",
        "text": "Do you feel pressure to respond or stay constantly updated?",
        "options": [
            "No pressure at all",
            "Mild pressure",
            "Quite often",
            "Constantly"
        ]
    },
    {
        "id": "twitter_wellbeing",
        "text": "Does Twitter support or hinder your daily focus and well-being?",
        "options": [
            "It helps me stay sharp and informed",
            "It's neutral",
            "It's a bit distracting",
            "It affects my focus significantly"
        ]
    },
    {
        "id": "twitter_safety",
        "text": "How safe or respected do you feel on Twitter?",
        "options": [
            "Very safe and respected",
            "Mostly okay",
            "Sometimes judged or misunderstood",
            "Often exposed to negativity"
        ]
    },
    {
        "id": "twitter_strategies",
        "text": "Are you open to strategies that help reduce online stress?",
        "options": [
            "Definitely",
            "Maybe",
            "I'm thinking about it",
            "Not right now"
        ]
    }
]

# YouTube Questionnaire
youtube_questions = [
    {
        "id": "youtube_frequency",
        "text": "How much time do you spend on YouTube daily?",
        "options": [
            "Less than 30 minutes",
            "30 minutes to 1 hour",
            "1-2 hours",
            "More than 2 hours"
        ]
    },
    {
        "id": "youtube_content",
        "text": "What type of content do you typically watch?",
        "options": [
            "Educational/informational",
            "Entertainment/comedy",
            "Music/relaxation",
            "Mixed content"
        ]
    },
    {
        "id": "youtube_behavior",
        "text": "How do you usually navigate YouTube?",
        "options": [
            "I search for specific videos",
            "I browse my subscriptions",
            "I follow recommended videos",
            "I watch trending content"
        ]
    },
    {
        "id": "youtube_feelings",
        "text": "How do you feel after watching YouTube?",
        "options": [
            "Informed or inspired",
            "Entertained and relaxed",
            "Sometimes distracted",
            "Often like I've wasted time"
        ]
    },
    {
        "id": "youtube_breaks",
        "text": "Do you take breaks between videos?",
        "options": [
            "Yes, regularly",
            "Sometimes",
            "Rarely",
            "I usually watch continuously"
        ]
    },
    {
        "id": "youtube_comparison",
        "text": "Do you ever compare yourself to content creators?",
        "options": [
            "Never",
            "Occasionally",
            "Sometimes",
            "Frequently"
        ]
    },
    {
        "id": "youtube_balance",
        "text": "How well do you balance YouTube with other activities?",
        "options": [
            "Very well - it's just one of many activities",
            "Fairly well",
            "Could be better",
            "It often takes priority over other things"
        ]
    },
    {
        "id": "youtube_sleep",
        "text": "Does YouTube ever affect your sleep?",
        "options": [
            "Never",
            "Rarely",
            "Sometimes",
            "Often"
        ]
    },
    {
        "id": "youtube_suggestions",
        "text": "Would you like suggestions for healthier YouTube habits?",
        "options": [
            "Yes, definitely",
            "Maybe",
            "Not sure",
            "No"
        ]
    }
]

# General Mood Questionnaire
general_questions = [
    {
        "id": "mood",
        "text": "How are you *really* feeling today?",
        "type": "emoji",
        "options": [
            {"label": "Great", "value": 5, "emoji": "😄"},
            {"label": "Good", "value": 4, "emoji": "🙂"},
            {"label": "Neutral", "value": 3, "emoji": "😐"},
            {"label": "Low", "value": 2, "emoji": "😔"},
            {"label": "Struggling", "value": 1, "emoji": "😢"}
        ]
    },
    {
        "id": "sleep",
        "text": "How was your sleep?",
        "type": "slider",
        "min": 1,
        "max": 5,
        "help": "1 = Poor sleep, 5 = Great sleep"
    },
    {
        "id": "stress",
        "text": "What's your stress level today?",
        "type": "slider",
        "min": 1,
        "max": 5,
        "help": "1 = Very low stress, 5 = Very high stress"
    },
    {
        "id": "anxiety",
        "text": "Did you feel anxious today?",
        "type": "boolean",
        "options": ["No", "Yes"]
    }
]

def display_platform_question(question, question_idx, total_questions):
    """Display a platform-specific question with its options"""
    st.markdown(f"### {question_idx+1}. {question['text']}")
    
    # Display options as buttons in columns
    option_cols = st.columns(len(question['options']))
    for i, option in enumerate(question['options']):
        with option_cols[i]:
            if st.button(option, key=f"{question['id']}_{i}", use_container_width=True):
                # Store response
                st.session_state["current_responses"][question['id']] = option
                
                # If this is the last question, save and redirect
                if question_idx == total_questions - 1:
                    # Add platform information
                    platform = st.session_state.get("selected_platform", None)
                    st.session_state["current_responses"]["platform"] = platform
                    
                    # For metrics calculation
                    # Convert detailed responses to standard mood metrics
                    if platform == "Instagram":
                        map_instagram_responses_to_metrics()
                    elif platform == "Facebook":
                        map_facebook_responses_to_metrics()
                    elif platform == "Twitter":
                        map_twitter_responses_to_metrics()
                    elif platform == "Snapchat":
                        map_snapchat_responses_to_metrics()
                    elif platform == "YouTube":
                        map_youtube_responses_to_metrics()
                        
                    save_and_redirect()
                else:
                    # Move to next question
                    st.session_state["current_step"] = question_idx + 2  # +2 because steps start from 1
                    st.rerun()

def map_instagram_responses_to_metrics():
    """Map Instagram responses to standard mood metrics"""
    responses = st.session_state["current_responses"]
    
    # Map feeling after use to mood (1-5 scale)
    feeling_map = {
        "Energized and positive": 5,
        "Neutral": 3,
        "Slightly distracted": 2,
        "Emotionally drained or overstimulated": 1
    }
    if "instagram_feeling" in responses:
        responses["mood"] = feeling_map.get(responses["instagram_feeling"], 3)
    
    # Map boundaries question to stress level (1-5 scale)
    boundaries_map = {
        "I already take breaks regularly": 1,
        "I've considered it but haven't started": 3,
        "It's hard to step away": 4,
        "I'd like help creating healthy boundaries": 3
    }
    if "instagram_boundaries" in responses:
        responses["stress"] = boundaries_map.get(responses["instagram_boundaries"], 3)
    
    # Map self-image influence to anxiety (boolean)
    anxiety_map = {
        "Not really": False,
        "Sometimes I feel inspired, other times unsure": False,
        "Yes, I've reflected more on how I view myself": False,
        "Yes, and I'm looking to understand this better": True
    }
    if "instagram_self_image" in responses:
        responses["anxiety"] = anxiety_map.get(responses["instagram_self_image"], False)

def map_facebook_responses_to_metrics():
    """Map Facebook responses to standard mood metrics"""
    responses = st.session_state["current_responses"]
    
    # Map feeling after use to mood (1-5 scale)
    feeling_map = {
        "Connected and positive": 5,
        "Neutral": 3,
        "Slightly distracted or overwhelmed": 2,
        "Anxious or left out": 1
    }
    if "facebook_feeling" in responses:
        responses["mood"] = feeling_map.get(responses["facebook_feeling"], 3)
    
    # Map emotional reactions to stress level (1-5 scale)
    emotional_map = {
        "Not at all": 1,
        "Slightly": 2,
        "Often": 4,
        "Strongly": 5
    }
    if "facebook_emotional" in responses:
        responses["stress"] = emotional_map.get(responses["facebook_emotional"], 3)
    
    # Map comparison to anxiety (boolean)
    anxiety_map = {
        "Not at all": False,
        "Occasionally": False,
        "Frequently": True,
        "Almost always": True
    }
    if "facebook_comparison" in responses:
        responses["anxiety"] = anxiety_map.get(responses["facebook_comparison"], False)

def map_twitter_responses_to_metrics():
    """Map Twitter responses to standard mood metrics"""
    responses = st.session_state["current_responses"]
    
    # Map feeling after use to mood (1-5 scale)
    feeling_map = {
        "Informed and curious": 5,
        "Neutral or unaffected": 3,
        "A bit overwhelmed or reactive": 2,
        "Emotionally unsettled": 1
    }
    if "twitter_feeling" in responses:
        responses["mood"] = feeling_map.get(responses["twitter_feeling"], 3)
    
    # Map arguments impact to stress level (1-5 scale)
    arguments_map = {
        "Not at all": 1,
        "Occasionally": 2,
        "Yes, they sometimes affect me": 4,
        "Yes, quite significantly": 5
    }
    if "twitter_arguments" in responses:
        responses["stress"] = arguments_map.get(responses["twitter_arguments"], 3)
    
    # Map pressure to respond to anxiety (boolean)
    pressure_map = {
        "No pressure at all": False,
        "Mild pressure": False,
        "Quite often": True,
        "Constantly": True
    }
    if "twitter_pressure" in responses:
        responses["anxiety"] = pressure_map.get(responses["twitter_pressure"], False)

def map_snapchat_responses_to_metrics():
    """Map Snapchat responses to standard mood metrics"""
    responses = st.session_state["current_responses"]
    
    # Map emotional state to mood (1-5 scale)
    emotional_map = {
        "I feel happy and connected": 5,
        "Neutral": 3,
        "Mixed emotions": 2,
        "Emotionally drained sometimes": 1
    }
    if "snapchat_emotional" in responses:
        responses["mood"] = emotional_map.get(responses["snapchat_emotional"], 3)
    
    # Map streaks breaking to stress level (1-5 scale)
    streaks_map = {
        "Unaffected": 1,
        "Slightly concerned": 2,
        "Stressed or anxious": 4,
        "Upset or emotional": 5
    }
    if "snapchat_streaks" in responses:
        responses["stress"] = streaks_map.get(responses["snapchat_streaks"], 3)
    
    # Map FOMO to anxiety (boolean)
    fomo_map = {
        "Never": False,
        "Rarely": False,
        "Sometimes": True,
        "Often": True
    }
    if "snapchat_fomo" in responses:
        responses["anxiety"] = fomo_map.get(responses["snapchat_fomo"], False)

def map_youtube_responses_to_metrics():
    """Map YouTube responses to standard mood metrics"""
    responses = st.session_state["current_responses"]
    
    # Map feeling after use to mood (1-5 scale)
    feeling_map = {
        "Informed or inspired": 5,
        "Entertained and relaxed": 4,
        "Sometimes distracted": 2,
        "Often like I've wasted time": 1
    }
    if "youtube_feelings" in responses:
        responses["mood"] = feeling_map.get(responses["youtube_feelings"], 3)
    
    # Map balance to stress level (1-5 scale)
    balance_map = {
        "Very well - it's just one of many activities": 1,
        "Fairly well": 2,
        "Could be better": 3,
        "It often takes priority over other things": 5
    }
    if "youtube_balance" in responses:
        responses["stress"] = balance_map.get(responses["youtube_balance"], 3)
    
    # Map sleep impact to anxiety (boolean)
    sleep_map = {
        "Never": False,
        "Rarely": False,
        "Sometimes": True,
        "Often": True
    }
    if "youtube_sleep" in responses:
        responses["anxiety"] = sleep_map.get(responses["youtube_sleep"], False)

# Main function
def main():
    st.markdown("<h1 style='text-align: center;'>Daily Mental Health Check</h1>", unsafe_allow_html=True)
    st.write("Let's take a moment to reflect on how you're feeling today")
    
    # Initialize or get the current step
    current_step = st.session_state.get("current_step", 1)
    
    # Get selected platform (if any)
    platform = st.session_state.get("selected_platform", None)
    
    # Determine which questionnaire to use based on platform
    if platform == "Instagram":
        questions = instagram_questions
        emoji_prefix = "📸 "
    elif platform == "Facebook":
        questions = facebook_questions
        emoji_prefix = "📘 "
    elif platform == "Twitter":
        questions = twitter_questions
        emoji_prefix = "🐦 "
    elif platform == "Snapchat":
        questions = snapchat_questions
        emoji_prefix = "👻 "
    elif platform == "YouTube":
        questions = youtube_questions
        emoji_prefix = "🎬 "
    else:
        questions = general_questions
        emoji_prefix = ""
    
    # Set total steps based on questionnaire
    if platform:
        # For platform-specific assessments, we show one question at a time
        total_steps = len(questions)
    else:
        # For general assessment, we group questions by category
        total_steps = 4  # Mood, Sleep, Stress & Anxiety, Final thoughts
    
    # Display progress bar
    display_progress_bar(current_step, total_steps)
    
    # Platform-specific text
    platform_text = f" for {platform}" if platform else ""
    
    if platform:
        # Platform-specific questionnaire (one question per step)
        st.subheader(f"{emoji_prefix}{platform} Usage{platform_text}")
        
        # Adjust current_step to be 0-indexed for array access
        question_idx = current_step - 1
        
        # Display current question if within range
        if 0 <= question_idx < len(questions):
            display_platform_question(questions[question_idx], question_idx, len(questions))
    else:
        # General mood questionnaire (grouped by category)
        # Step 1: Mood
        if current_step == 1:
            st.subheader(f"Step {current_step} of {total_steps}: General Mood Check{platform_text}")
            
            # Question 1: Mood (emoji scale)
            mood_question = general_questions[0]
            st.markdown(f"### {mood_question['text']}")
            
            emoji_cols = st.columns(5)
            for i, option in enumerate(mood_question['options']):
                with emoji_cols[i]:
                    if st.button(option['emoji'], key=f"mood_{option['value']}", help=option['label']):
                        st.session_state["current_responses"]["mood"] = option['value']
                        st.session_state["current_step"] = 2
                        st.rerun()
        
        # Step 2: Sleep
        elif current_step == 2:
            st.subheader(f"Step {current_step} of {total_steps}: Sleep & Rest{platform_text}")
            
            # Question: Sleep quality (slider)
            sleep_question = general_questions[1]
            st.markdown(f"### {sleep_question['text']}")
            sleep_value = st.slider(
                "Drag the slider", 
                min_value=sleep_question['min'], 
                max_value=sleep_question['max'],
                value=3,
                step=1,
                help=sleep_question['help'],
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
            
            # Question: Stress level (slider)
            stress_question = general_questions[2]
            st.markdown(f"### {stress_question['text']}")
            stress_value = st.slider(
                "Drag the slider", 
                min_value=stress_question['min'], 
                max_value=stress_question['max'],
                value=3,
                step=1,
                help=stress_question['help'],
                label_visibility="collapsed"
            )
            st.session_state["current_responses"]["stress"] = stress_value
            
            # Question: Anxiety (boolean)
            anxiety_question = general_questions[3]
            st.markdown(f"### {anxiety_question['text']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(anxiety_question['options'][0], key="anxiety_no", use_container_width=True):
                    st.session_state["current_responses"]["anxiety"] = False
                    st.session_state["current_step"] = 4
                    st.rerun()
            with col2:
                if st.button(anxiety_question['options'][1], key="anxiety_yes", use_container_width=True):
                    st.session_state["current_responses"]["anxiety"] = True
                    st.session_state["current_step"] = 4
                    st.rerun()
        
        # Step 4: Final thoughts
        elif current_step == 4:
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
