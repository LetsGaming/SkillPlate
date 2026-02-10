from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import authenticate_user, generate_user_tokens, refresh_access_token
from app.utils.responses import success_response, error_response

# Variable name matches the dynamic loader's expected naming convention
auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return error_response("Missing request body", 400)

    username = data.get("username")
    password = data.get("password")

    # 1. Verify credentials via Service
    user = authenticate_user(username, password)
    if not user:
        return error_response("Invalid username or password", 401)

    # 2. Generate tokens via Service
    tokens = generate_user_tokens(user["id"])
    
    return success_response(
        data=tokens, 
        message="Login successful"
    )

@auth_routes.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    Endpoint to exchange a refresh token for a new access token.
    """
    current_user_id = get_jwt_identity()
    new_token = refresh_access_token(current_user_id)
    
    return success_response(
        data={"access_token": new_token},
        message="Token refreshed"
    )