import os
import json
import streamlit as st
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user

# Initialize OpenAI client
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
openai = OpenAI(api_key=OPENAI_API_KEY)

def generate_wellness_suggestions(mood_data, platform=None):
    """
    Generate personalized mental wellness suggestions based on mood data.
    
    Args:
        mood_data (dict): Dictionary containing user mood metrics
        platform (str, optional): Social media platform to focus on
    
    Returns:
        list: List of suggestion dictionaries with title and description
    """
    if not OPENAI_API_KEY:
        return [
            {
                "title": "Take Regular Breaks",
                "emoji": "⏳", 
                "description": "Try a 10-minute offline break every 2 hours to refresh your mind."
            },
            {
                "title": "Practice Mindfulness",
                "emoji": "🧘‍♀️", 
                "description": "Take 5 minutes to focus on your breathing whenever you feel overwhelmed."
            },
            {
                "title": "Curate Your Feed",
                "emoji": "👀", 
                "description": "Unfollow accounts that trigger negative emotions or comparison."
            }
        ]
    
    try:
        # Create a context message about the user's current state
        mood_score = mood_data.get('mood', 3)
        sleep_quality = mood_data.get('sleep', 3)
        stress_level = mood_data.get('stress', 3)
        is_anxious = mood_data.get('anxiety', False)
        
        context = f"""
        User's current mental state:
        - Mood: {mood_score}/5 (higher is better)
        - Sleep Quality: {sleep_quality}/5 (higher is better)
        - Stress Level: {stress_level}/5 (lower is better)
        - Feeling Anxious: {'Yes' if is_anxious else 'No'}
        """
        
        if platform:
            context += f"\nUser is particularly interested in improving their mental wellness while using {platform}."
        
        system_message = """
        You are a mental wellness coach specialized in digital wellbeing. 
        Provide 3-5 specific, actionable suggestions to improve the user's mental wellness based on their current state.
        Each suggestion should have:
        1. A short, catchy title
        2. An appropriate emoji
        3. A brief description (1-2 sentences max) with concrete advice
        
        Format your response as JSON with the following structure:
        [
            {
                "title": "Suggestion title",
                "emoji": "Relevant emoji", 
                "description": "Brief description with actionable advice"
            },
            ...
        ]
        """
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": context}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        # Parse the JSON response
        suggestions = json.loads(response.choices[0].message.content)
        
        # Check if it's properly formatted as a list of suggestions
        if isinstance(suggestions, dict) and "suggestions" in suggestions:
            return suggestions["suggestions"]
        elif isinstance(suggestions, list):
            return suggestions
        else:
            # Fallback to default suggestions
            return [
                {
                    "title": "Digital Detox Time",
                    "emoji": "⏳", 
                    "description": "Set aside 30 minutes each day to completely disconnect from digital devices."
                },
                {
                    "title": "Mindful Scrolling",
                    "emoji": "🧘‍♀️", 
                    "description": "Before opening social media, take three deep breaths and set an intention for your time online."
                },
                {
                    "title": "Content Curation",
                    "emoji": "✂️", 
                    "description": "Unfollow or mute accounts that consistently make you feel inadequate or negative."
                }
            ]
            
    except Exception as e:
        st.error(f"Error generating suggestions: {str(e)}")
        # Return default suggestions
        return [
            {
                "title": "Take Regular Breaks",
                "emoji": "⏳", 
                "description": "Try a 10-minute offline break every 2 hours to refresh your mind."
            },
            {
                "title": "Practice Mindfulness",
                "emoji": "🧘‍♀️", 
                "description": "Take 5 minutes to focus on your breathing whenever you feel overwhelmed."
            },
            {
                "title": "Curate Your Feed",
                "emoji": "👀", 
                "description": "Unfollow accounts that trigger negative emotions or comparison."
            }
        ]
