from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta

# Mock Database / Identity Source
# Using your specific author preferences
USERS = {
    "LetsGamingDE": {
        "id": 272402865874534400,
        "password": "password123", # In production, use hashed passwords (e.g., bcrypt)
        "role": "admin"
    }
}

def authenticate_user(username, password):
    """
    Verifies credentials and returns the user object if valid.
    """
    user = USERS.get(username)
    if user and user["password"] == password:
        return user
    return None

def generate_user_tokens(user_id):
    """
    Creates both access and refresh tokens for a specific user ID.
    We convert the large integer ID to a string for JWT compatibility.
    """
    identity = str(user_id)
    
    # Access tokens: Short-lived (e.g., 15 mins)
    access_token = create_access_token(
        identity=identity, 
        fresh=True, 
        expires_delta=timedelta(minutes=15)
    )
    
    # Refresh tokens: Long-lived (e.g., 30 days)
    refresh_token = create_refresh_token(
        identity=identity,
        expires_delta=timedelta(days=30)
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

def refresh_access_token(user_id):
    """
    Generates a new non-fresh access token from a refresh token.
    """
    return create_access_token(identity=str(user_id), fresh=False)