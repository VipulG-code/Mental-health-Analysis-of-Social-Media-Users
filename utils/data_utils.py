import streamlit as st
import pandas as pd
import datetime
import random
import os
import json
import joblib
import numpy as np
from assets.quotes import motivational_quotes

# Set up data directory
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if "user_name" not in st.session_state:
        st.session_state["user_name"] = ""
    
    if "mood_data" not in st.session_state:
        st.session_state["mood_data"] = []
    
    if "current_responses" not in st.session_state:
        st.session_state["current_responses"] = {}
    
    if "selected_platform" not in st.session_state:
        st.session_state["selected_platform"] = None
    
    if "ai_suggestions" not in st.session_state:
        st.session_state["ai_suggestions"] = []
        
    if "current_step" not in st.session_state:
        st.session_state["current_step"] = 1
    
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None
    
    if "user_email" not in st.session_state:
        st.session_state["user_email"] = None

def save_user_data(responses):
    """Save user response data to session state and data file"""
    # Add timestamp
    responses["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Add ML-based wellbeing score prediction
    ml_score = predict_ml_score(responses)
    if ml_score:
        responses["ml_wellbeing_score"] = ml_score
    
    # Save to session state
    st.session_state["mood_data"].append(responses)
    
    # Save to user's data file if authenticated
    if st.session_state.get("authenticated") and st.session_state.get("user_id"):
        user_data_file = os.path.join(DATA_DIR, f"user_{st.session_state['user_id']}.json")
        try:
            if os.path.exists(user_data_file):
                with open(user_data_file, "r") as f:
                    user_data = json.load(f)
            else:
                user_data = {}
            
            user_data["mood_data"] = st.session_state["mood_data"]
            
            with open(user_data_file, "w") as f:
                json.dump(user_data, f)
        except Exception as e:
            st.error(f"Error saving user data: {e}")
    
    # Save to common dataset for ML training
    save_to_ml_dataset(responses)
    
    # Reset current responses and step
    st.session_state["current_responses"] = {}
    st.session_state["current_step"] = 1

def save_to_ml_dataset(responses):
    """Append response data to a common dataset for ML training"""
    ml_dataset_file = os.path.join(DATA_DIR, "ml_dataset.json")
    
    try:
        if os.path.exists(ml_dataset_file):
            with open(ml_dataset_file, "r") as f:
                try:
                    dataset = json.load(f)
                except json.JSONDecodeError:
                    dataset = {"responses": []}
        else:
            dataset = {"responses": []}
        
        dataset["responses"].append(responses)
        
        with open(ml_dataset_file, "w") as f:
            json.dump(dataset, f)
    except Exception as e:
        print(f"Error saving to ML dataset: {e}")

def get_mood_data_as_df():
    """Convert mood data to pandas DataFrame for visualization"""
    if not st.session_state.get("mood_data", []):
        return pd.DataFrame()
    
    # Convert to DataFrame
    df = pd.DataFrame(st.session_state["mood_data"])
    
    # Convert date string to datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
    
    return df

def get_random_quote():
    """Return a random motivational quote"""
    quote_entry = random.choice(motivational_quotes)
    return quote_entry["quote"], quote_entry["author"]

def calculate_wellbeing_score(data):
    """Calculate an overall wellbeing score based on mood data"""
    # Check if data is a pandas Series or DataFrame
    if hasattr(data, 'to_dict'):
        data = data.to_dict()
    
    if not data:
        return 0
    
    # Use ML score if available
    if "ml_wellbeing_score" in data:
        ml_score = data["ml_wellbeing_score"]
        # Handle NaN or None values
        if ml_score is None or (isinstance(ml_score, float) and pd.isna(ml_score)):
            ml_score = 0
        try:
            return int(ml_score)
        except (ValueError, TypeError):
            return 0
    
    try:
        # Extract relevant metrics (with NaN handling)
        mood = data.get('mood', 3)
        if mood is None or (isinstance(mood, float) and pd.isna(mood)):
            mood = 3
        
        sleep = data.get('sleep', 3)
        if sleep is None or (isinstance(sleep, float) and pd.isna(sleep)):
            sleep = 3
        
        stress = data.get('stress', 3)
        if stress is None or (isinstance(stress, float) and pd.isna(stress)):
            stress = 3
        stress = 6 - stress  # Invert stress so higher is better
        
        anxiety = data.get('anxiety', False)
        if anxiety is None or (isinstance(anxiety, float) and pd.isna(anxiety)):
            anxiety = False
        anxiety = 0 if anxiety else 1  # 0 if anxious, 1 if not
        
        # Calculate weighted average (adjust weights as needed)
        wellbeing_score = (float(mood) * 0.4) + (float(sleep) * 0.3) + (float(stress) * 0.2) + (float(anxiety) * 0.1)
        
        # Convert to 0-100 scale
        return int(round((wellbeing_score / 5) * 100))
    except Exception as e:
        print(f"Error calculating wellbeing score: {e}")
        return 0

def train_ml_model():
    """Train a machine learning model on the collected data"""
    ml_dataset_file = os.path.join(DATA_DIR, "ml_dataset.json")
    model_file = os.path.join(DATA_DIR, "wellbeing_model.pkl")
    
    if not os.path.exists(ml_dataset_file):
        return False
    
    try:
        with open(ml_dataset_file, "r") as f:
            dataset = json.load(f)
        
        if len(dataset["responses"]) < 5:  # Need at least 5 data points
            return False
        
        # Convert to DataFrame
        df = pd.DataFrame(dataset["responses"])
        
        # Extract features
        features = []
        target = []
        
        for _, row in df.iterrows():
            # Basic features
            feature_dict = {
                "mood": row.get("mood", 3),
                "sleep": row.get("sleep", 3),
                "stress": row.get("stress", 3),
                "anxiety": 1 if row.get("anxiety", False) else 0
            }
            
            # Add platform-specific features if available
            if "platform" in row:
                platform = row["platform"].lower() if row["platform"] else "none"
                feature_dict["platform_" + platform] = 1
                
                # Add time spent on platform if available
                if "platform_time" in row:
                    time_mapping = {
                        "Less than 30 minutes": 1,
                        "30 minutes to 1 hour": 2,
                        "1-2 hours": 3,
                        "2-3 hours": 4,
                        "More than 3 hours": 5
                    }
                    feature_dict["platform_time"] = time_mapping.get(row["platform_time"], 3)
                
                # Add content impact if available
                if "content_impact" in row:
                    impact_mapping = {
                        "Positive": 1,
                        "Neutral": 0,
                        "Negative": -1
                    }
                    feature_dict["content_impact"] = impact_mapping.get(row["content_impact"], 0)
            
            features.append(feature_dict)
            
            # Calculate traditional wellbeing score as target
            mood = row.get("mood", 3)
            sleep = row.get("sleep", 3)
            stress = 6 - row.get("stress", 3)  # Invert stress so higher is better
            anxiety = 0 if row.get("anxiety", False) else 1  # 0 if anxious, 1 if not
            
            wellbeing_score = (mood * 0.4) + (sleep * 0.3) + (stress * 0.2) + (anxiety * 0.1)
            target.append(round((wellbeing_score / 5) * 100))
        
        # Convert to DataFrame for scikit-learn
        X = pd.DataFrame(features).fillna(0)
        y = np.array(target)
        
        # Handle categorical variables
        X = pd.get_dummies(X, drop_first=True)
        
        # Train a simple model (Linear Regression)
        from sklearn.linear_model import LinearRegression
        from sklearn.preprocessing import StandardScaler
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        model = LinearRegression()
        model.fit(X_scaled, y)
        
        # Save model and scaler
        joblib.dump((model, scaler, list(X.columns)), model_file)
        
        return True
    except Exception as e:
        print(f"Error training ML model: {e}")
        return False

def predict_ml_score(data):
    """Predict wellbeing score using the trained ML model"""
    model_file = os.path.join(DATA_DIR, "wellbeing_model.pkl")
    
    if not os.path.exists(model_file):
        # Try to train the model first
        if train_ml_model():
            # If training succeeded, the model file should exist now
            if not os.path.exists(model_file):
                return None
        else:
            return None
    
    try:
        # Load model
        model, scaler, feature_names = joblib.load(model_file)
        
        # Extract features from data
        feature_dict = {
            "mood": data.get("mood", 3),
            "sleep": data.get("sleep", 3),
            "stress": data.get("stress", 3),
            "anxiety": 1 if data.get("anxiety", False) else 0
        }
        
        # Add platform-specific features if available
        if "platform" in data:
            platform = data["platform"].lower() if data["platform"] else "none"
            feature_dict["platform_" + platform] = 1
            
            # Add time spent on platform if available
            if "platform_time" in data:
                time_mapping = {
                    "Less than 30 minutes": 1,
                    "30 minutes to 1 hour": 2,
                    "1-2 hours": 3,
                    "2-3 hours": 4,
                    "More than 3 hours": 5
                }
                feature_dict["platform_time"] = time_mapping.get(data["platform_time"], 3)
            
            # Add content impact if available
            if "content_impact" in data:
                impact_mapping = {
                    "Positive": 1,
                    "Neutral": 0,
                    "Negative": -1
                }
                feature_dict["content_impact"] = impact_mapping.get(data["content_impact"], 0)
        
        # Convert to DataFrame
        X = pd.DataFrame([feature_dict]).fillna(0)
        
        # Handle categorical variables and match the training columns
        X = pd.get_dummies(X, drop_first=True)
        
        # Ensure all columns from training are present
        for col in feature_names:
            if col not in X.columns:
                X[col] = 0
        
        # Keep only the columns used during training
        X = X[feature_names]
        
        # Scale features
        X_scaled = scaler.transform(X)
        
        # Predict
        prediction = model.predict(X_scaled)[0]
        
        # Ensure prediction is in 0-100 range
        prediction = max(0, min(100, prediction))
        
        return round(prediction)
    except Exception as e:
        print(f"Error predicting ML score: {e}")
        return None

def export_user_data_csv():
    """Export user's mood data to CSV file"""
    if not st.session_state.get("authenticated") or not st.session_state.get("user_id"):
        return None
    
    if not st.session_state.get("mood_data", []):
        return None
    
    try:
        # Convert to DataFrame
        df = pd.DataFrame(st.session_state["mood_data"])
        
        # Create export directory if it doesn't exist
        export_dir = os.path.join(DATA_DIR, "exports")
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        
        # Generate filename
        filename = f"mental_wellness_data_user_{st.session_state['user_id']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(export_dir, filename)
        
        # Save to CSV
        df.to_csv(filepath, index=False)
        
        return filepath
    except Exception as e:
        st.error(f"Error exporting data: {e}")
        return None