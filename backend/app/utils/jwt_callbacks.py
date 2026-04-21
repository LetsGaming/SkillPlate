from app.utils.responses import error_response

def register_jwt_callbacks(jwt):
    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        # error_string contains the reason (e.g., "Signature verification failed")
        return error_response(f"Invalid token: {error_string}", 401)

    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        return error_response("Authorization header missing or malformed", 401)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return error_response("Token has expired", 401)
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return error_response("Token has been revoked", 401)