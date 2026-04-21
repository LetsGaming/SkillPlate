from flask import jsonify, make_response

def api_response(success=True, message=None, data=None, status_code=200):
    """
    Unified API response format.
    """
    response_body = {
        "success": success,
        "message": message,
        "data": data
    }
    
    # Optional: Add a timestamp or request ID here
    return make_response(jsonify(response_body), status_code)

def success_response(data=None, message="Success", status_code=200):
    return api_response(True, message, data, status_code)

def error_response(message="An error occurred", status_code=400, data=None):
    return api_response(False, message, data, status_code)