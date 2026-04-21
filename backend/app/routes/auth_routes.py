from flask import Blueprint, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    set_refresh_cookies,
    unset_jwt_cookies
)

from backend.app.services.auth_service import authenticate_user, generate_user_tokens, refresh_access_token
from backend.app.utils.responses import success_response, error_response

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return error_response("Missing request body", 400)

    username = data.get("username")
    password = data.get("password")

    # 1. Verify credentials
    user = authenticate_user(username, password)
    if not user:
        return error_response("Invalid username or password", 401)

    # 2. Generate tokens
    # Assuming generate_user_tokens returns {"access_token": "...", "refresh_token": "..."}
    tokens = generate_user_tokens(user["id"])
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    # 3. Create response and set HttpOnly Cookie
    response = success_response(
        data={"access_token": access_token}, 
        message="Login successful"
    )
    
    # This helper sets the 'refresh_token_cookie' automatically based on your app config
    set_refresh_cookies(response, refresh_token)
    
    return response

@auth_routes.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    Endpoint to exchange a refresh token (from cookie) for a new access token.
    """
    current_user_id = get_jwt_identity()
    new_access_token = refresh_access_token(current_user_id)
    
    return success_response(
        data={"access_token": new_access_token},
        message="Token refreshed"
    )

@auth_routes.route("/logout", methods=["POST"])
def logout():
    """
    Clear cookies on logout.
    """
    response = success_response(message="Logout successful")
    unset_jwt_cookies(response)
    return response