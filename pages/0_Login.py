import streamlit as st
import json
import os
import hashlib
import re
from utils.data_utils import initialize_session_state

# Page configuration
st.set_page_config(
    page_title="Login | Mental Wellness Tracker",
    page_icon="🌱",
    layout="wide"
)

# Initialize session state
initialize_session_state()

# Set up data directory if it doesn't exist
DATA_DIR = "data"
USER_DATA_FILE = os.path.join(DATA_DIR, "users.json")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    """Load user data from JSON file"""
    try:
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_users(users):
    """Save user data to JSON file"""
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f)

def hash_password(password):
    """Create a secure hash of the password"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """Validate email format"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    # Check for at least one uppercase, one lowercase, and one digit
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit"
    
    return True, "Password is strong"

def main():
    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        st.switch_page("app.py")
    
    st.markdown("<h1 style='text-align: center;'>Mental Wellness Tracker</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("## Login")
        
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        login_button = st.button("Login", type="primary", use_container_width=True)
        
        if login_button:
            if not login_email or not login_password:
                st.error("Please enter both email and password")
            else:
                users = load_users()
                
                if login_email in users and users[login_email]["password"] == hash_password(login_password):
                    st.session_state["authenticated"] = True
                    st.session_state["user_email"] = login_email
                    st.session_state["user_name"] = users[login_email]["name"]
                    st.session_state["user_id"] = users[login_email]["id"]
                    
                    # Load user mood data if exists
                    user_data_file = os.path.join(DATA_DIR, f"user_{users[login_email]['id']}.json")
                    if os.path.exists(user_data_file):
                        try:
                            with open(user_data_file, "r") as f:
                                user_data = json.load(f)
                                st.session_state["mood_data"] = user_data.get("mood_data", [])
                        except (json.JSONDecodeError, FileNotFoundError):
                            st.session_state["mood_data"] = []
                    
                    st.success("Login successful!")
                    st.switch_page("app.py")
                else:
                    st.error("Invalid email or password")
    
    with col2:
        st.markdown("## Sign Up")
        
        signup_name = st.text_input("Full Name", key="signup_name")
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_password")
        signup_confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
        
        signup_button = st.button("Sign Up", use_container_width=True)
        
        if signup_button:
            if not signup_name or not signup_email or not signup_password or not signup_confirm_password:
                st.error("Please fill out all fields")
            elif not validate_email(signup_email):
                st.error("Please enter a valid email address")
            elif signup_password != signup_confirm_password:
                st.error("Passwords do not match")
            else:
                password_valid, message = validate_password(signup_password)
                if not password_valid:
                    st.error(message)
                else:
                    users = load_users()
                    
                    if signup_email in users:
                        st.error("Email already exists. Please use a different email or login.")
                    else:
                        # Generate a unique user ID
                        user_id = str(len(users) + 1).zfill(6)
                        
                        # Add the new user
                        users[signup_email] = {
                            "id": user_id,
                            "name": signup_name,
                            "password": hash_password(signup_password),
                            "created_at": str(pd.Timestamp.now())
                        }
                        
                        save_users(users)
                        
                        # Create user data file
                        user_data_file = os.path.join(DATA_DIR, f"user_{user_id}.json")
                        with open(user_data_file, "w") as f:
                            json.dump({"mood_data": []}, f)
                        
                        st.success(f"Account created successfully for {signup_name}! Please login.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center;'>
        <p>Your mental wellness journey starts here.</p>
        <p>All data is stored securely and used only to provide personalized insights.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    import pandas as pd
    main()