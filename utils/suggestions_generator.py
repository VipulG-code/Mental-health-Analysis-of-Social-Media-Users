import random

def generate_instagram_suggestions(mood_data):
    """Generate Instagram-specific suggestions based on mood data."""
    suggestions = [
        {
            "title": "Curate Your Feed",
            "emoji": "✂️",
            "description": "Unfollow accounts that make you feel inadequate. Follow those that inspire genuine joy and creativity."
        },
        {
            "title": "Set Time Boundaries",
            "emoji": "⏱️",
            "description": "Use your phone's screen time feature to limit Instagram to 30 minutes per day."
        },
        {
            "title": "Mindful Scrolling",
            "emoji": "🧘‍♀️",
            "description": "Before opening Instagram, take three deep breaths and set an intention for what you want to get from the app."
        },
        {
            "title": "Reality Check",
            "emoji": "🔍",
            "description": "Remember that most Instagram posts show carefully curated highlights, not real everyday life."
        },
        {
            "title": "Engagement Detox",
            "emoji": "❤️",
            "description": "Try using Instagram without checking your likes or followers count for a week."
        },
        {
            "title": "Post Authentically",
            "emoji": "📸",
            "description": "Share a completely unfiltered, real moment from your day without worrying about likes."
        },
        {
            "title": "Comment Kindness",
            "emoji": "💬",
            "description": "Leave three genuine, supportive comments on friends' posts instead of just liking."
        }
    ]
    
    # Select 3-5 suggestions based on mood data
    if mood_data.get('mood', 3) <= 2 or mood_data.get('stress', 3) >= 4:
        # More supportive suggestions for lower mood or higher stress
        return random.sample(suggestions, min(5, len(suggestions)))
    else:
        return random.sample(suggestions, min(3, len(suggestions)))

def generate_facebook_suggestions(mood_data):
    """Generate Facebook-specific suggestions based on mood data."""
    suggestions = [
        {
            "title": "News Feed Cleanse",
            "emoji": "🧹",
            "description": "Use 'Take a Break' feature to see less of certain people without unfriending them."
        },
        {
            "title": "Groups Focus",
            "emoji": "👥",
            "description": "Spend more time in positive, hobby-based groups and less time on the main feed."
        },
        {
            "title": "Notification Detox",
            "emoji": "🔕",
            "description": "Turn off all non-essential notifications to reduce the urge to constantly check Facebook."
        },
        {
            "title": "Memory Lane Limits",
            "emoji": "🕰️",
            "description": "If 'On This Day' memories trigger negative emotions, adjust your settings to see fewer of them."
        },
        {
            "title": "Active vs. Passive",
            "emoji": "🏃‍♂️",
            "description": "Engage actively (posting, commenting) rather than passively scrolling, which research links to better wellbeing."
        },
        {
            "title": "Evening Boundary",
            "emoji": "🌙",
            "description": "Make your bedroom a Facebook-free zone, especially in the hour before sleep."
        },
        {
            "title": "Weekly Digital Sabbath",
            "emoji": "📵",
            "description": "Choose one day per week to stay completely off Facebook and focus on in-person connections."
        }
    ]
    
    if 'anxiety' in mood_data and mood_data['anxiety']:
        # Add more calming suggestions for users reporting anxiety
        suggestions.append({
            "title": "Compare Less, Connect More",
            "emoji": "🤝",
            "description": "When you notice comparison thoughts, message a friend to have a real conversation instead."
        })
    
    return random.sample(suggestions, min(4, len(suggestions)))

def generate_twitter_suggestions(mood_data):
    """Generate Twitter/X-specific suggestions based on mood data."""
    suggestions = [
        {
            "title": "Curate Your Timeline",
            "emoji": "✂️",
            "description": "Use mute words for topics that consistently trigger stress or negative emotions."
        },
        {
            "title": "Reply Timer",
            "emoji": "⏲️",
            "description": "Wait 5 minutes before responding to content that provokes a strong emotional reaction."
        },
        {
            "title": "Follow Diversity",
            "emoji": "🌈",
            "description": "Ensure your feed includes diverse perspectives to avoid echo chamber effects."
        },
        {
            "title": "Trending Topics Break",
            "emoji": "🛑",
            "description": "Avoid the Trending tab when you're already feeling stressed or anxious."
        },
        {
            "title": "Three-Tweet Rule",
            "emoji": "3️⃣",
            "description": "If you've opened Twitter three times in an hour, take a 30-minute break."
        },
        {
            "title": "Discussion Boundaries",
            "emoji": "🚧",
            "description": "It's okay to disengage from debates that become unproductive or hostile."
        },
        {
            "title": "Positive Contribution",
            "emoji": "✨",
            "description": "Share one positive or uplifting tweet for every critical one you post."
        }
    ]
    
    # Adjust number of suggestions based on stress level
    num_suggestions = 3
    if mood_data.get('stress', 3) >= 4:
        num_suggestions = 5
    
    return random.sample(suggestions, min(num_suggestions, len(suggestions)))

def generate_youtube_suggestions(mood_data):
    """Generate YouTube-specific suggestions based on mood data."""
    suggestions = [
        {
            "title": "Watch Intentionally",
            "emoji": "🎯",
            "description": "Search for specific videos rather than endlessly scrolling the recommended feed."
        },
        {
            "title": "Comment Mindfully",
            "emoji": "💬",
            "description": "Before posting a comment, ask yourself: Is it kind? Is it necessary? Is it helpful?"
        },
        {
            "title": "Clear Watch History",
            "emoji": "🧹",
            "description": "Periodically clear your watch history to reset the algorithm and get fresh recommendations."
        },
        {
            "title": "Set Time Limits",
            "emoji": "⏱️",
            "description": "Use YouTube's built-in reminders to take breaks after a set time period."
        },
        {
            "title": "Schedule Viewing",
            "emoji": "📅",
            "description": "Designate specific times for YouTube rather than using it as a default time-filler."
        },
        {
            "title": "Growth-Focused Content",
            "emoji": "🌱",
            "description": "Subscribe to channels that teach skills or knowledge relevant to your goals."
        },
        {
            "title": "Disable Autoplay",
            "emoji": "⏹️",
            "description": "Turn off autoplay to make conscious choices about what you watch next."
        }
    ]
    
    # Adjust suggestions based on sleep quality
    if mood_data.get('sleep', 3) <= 2:
        suggestions.append({
            "title": "Evening Screen Break",
            "emoji": "🌙",
            "description": "Avoid YouTube at least one hour before bedtime to improve sleep quality."
        })
    
    return random.sample(suggestions, min(4, len(suggestions)))

def generate_snapchat_suggestions(mood_data):
    """Generate Snapchat-specific suggestions based on mood data."""
    suggestions = [
        {
            "title": "Streak Freedom",
            "emoji": "🔥",
            "description": "Remember that streaks don't define friendships. It's okay if they break sometimes."
        },
        {
            "title": "Authentic Sharing",
            "emoji": "🤗",
            "description": "Share real moments instead of only curated ones. Authenticity strengthens connections."
        },
        {
            "title": "Story Boundaries",
            "emoji": "🛑",
            "description": "You don't need to watch everyone's stories every day. Be selective with your attention."
        },
        {
            "title": "FOMO Fighter",
            "emoji": "💪",
            "description": "When feeling left out, message a friend to arrange a real hangout instead of just watching."
        },
        {
            "title": "Snap Map Privacy",
            "emoji": "🗺️",
            "description": "Use Ghost Mode when needed - it's okay not to share your location all the time."
        },
        {
            "title": "Notification Pause",
            "emoji": "🔕",
            "description": "Turn off Snapchat notifications during study time, work, or when you need to focus."
        },
        {
            "title": "Content Intention",
            "emoji": "🧭",
            "description": "Before opening Snapchat, set an intention: 'I'm checking in with specific friends' rather than mindless browsing."
        }
    ]
    
    return random.sample(suggestions, min(4, len(suggestions)))

def generate_general_suggestions(mood_data):
    """Generate general digital wellbeing suggestions based on mood data."""
    suggestions = [
        {
            "title": "Digital Detox Time",
            "emoji": "⏳",
            "description": "Set aside 30 minutes each day to completely disconnect from digital devices."
        },
        {
            "title": "Morning Mindfulness",
            "emoji": "🌅",
            "description": "Wait 30 minutes after waking up before checking any social media apps."
        },
        {
            "title": "Nature Connection",
            "emoji": "🌳",
            "description": "When feeling overwhelmed by screen time, take a 10-minute walk outside without your phone."
        },
        {
            "title": "Bedtime Boundary",
            "emoji": "🛏️",
            "description": "Create a charging station outside your bedroom to avoid nighttime scrolling."
        },
        {
            "title": "Mindful Notifications",
            "emoji": "🔔",
            "description": "Turn off all non-essential app notifications to reduce digital distraction."
        },
        {
            "title": "Comparison Awareness",
            "emoji": "👁️",
            "description": "When you notice comparison thoughts, remind yourself you're seeing others' highlights, not their reality."
        },
        {
            "title": "Digital Sabbath",
            "emoji": "📵",
            "description": "Choose one day per month for a complete digital detox - no social media or unnecessary screen time."
        },
        {
            "title": "Focus Blocks",
            "emoji": "🧱",
            "description": "Use the Pomodoro technique: 25 minutes of focused work followed by 5 minutes of break time."
        }
    ]
    
    # Adjust based on mood, stress, and anxiety
    mood_score = mood_data.get('mood', 3)
    stress_level = mood_data.get('stress', 3)
    is_anxious = mood_data.get('anxiety', False)
    
    num_suggestions = 3
    if mood_score <= 2 or stress_level >= 4 or is_anxious:
        num_suggestions = 5
    
    return random.sample(suggestions, min(num_suggestions, len(suggestions)))

def generate_wellness_suggestions(mood_data, platform=None):
    """
    Generate personalized mental wellness suggestions based on mood data.
    
    Args:
        mood_data (dict): Dictionary containing user mood metrics
        platform (str, optional): Social media platform to focus on
    
    Returns:
        list: List of suggestion dictionaries with title and description
    """
    if platform == "Instagram":
        return generate_instagram_suggestions(mood_data)
    elif platform == "Facebook":
        return generate_facebook_suggestions(mood_data)
    elif platform == "Twitter":
        return generate_twitter_suggestions(mood_data)
    elif platform == "YouTube":
        return generate_youtube_suggestions(mood_data)
    elif platform == "Snapchat":
        return generate_snapchat_suggestions(mood_data)
    else:
        return generate_general_suggestions(mood_data)