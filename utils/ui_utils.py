import streamlit as st
from utils.data_utils import calculate_wellbeing_score

def display_emoji_scale(key, question_text):
    """Display an emoji-based mood scale"""
    st.markdown(f"### {question_text}")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("😢", key=f"{key}_1", use_container_width=True):
            return 1
    with col2:
        if st.button("😔", key=f"{key}_2", use_container_width=True):
            return 2
    with col3:
        if st.button("😐", key=f"{key}_3", use_container_width=True):
            return 3
    with col4:
        if st.button("🙂", key=f"{key}_4", use_container_width=True):
            return 4
    with col5:
        if st.button("😄", key=f"{key}_5", use_container_width=True):
            return 5
    
    return None

def display_wellbeing_score(data):
    """Display wellbeing score with appropriate styling"""
    score = calculate_wellbeing_score(data)
    
    # Determine color based on score
    if score >= 80:
        color = "#28a745"  # Green
        emoji = "🌟"
    elif score >= 60:
        color = "#17a2b8"  # Blue
        emoji = "✨"
    elif score >= 40:
        color = "#ffc107"  # Yellow
        emoji = "⚡"
    else:
        color = "#dc3545"  # Red
        emoji = "💪"
    
    st.markdown(f"""
    <div style='background-color: {color}; padding: 15px; border-radius: 10px; text-align: center;'>
        <h2 style='color: white; margin: 0;'>Wellbeing Score {emoji}</h2>
        <p style='font-size: 48px; margin: 10px 0; color: white;'>{score}</p>
        <p style='color: white;'>out of 100</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Return the score for further processing if needed
    return score

def display_progress_bar(current_step, total_steps):
    """Display a progress bar for multi-step forms"""
    progress = current_step / total_steps
    st.progress(progress)
    st.caption(f"Step {current_step} of {total_steps}")
