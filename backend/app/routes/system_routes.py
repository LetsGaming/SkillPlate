from flask import Blueprint
from app.utils.responses import success_response

system_routes = Blueprint("system_routes", __name__)

@system_routes.route('/api/hello', defaults={'name': None}, methods=['GET'])
@system_routes.route('/api/hello/<string:name>', methods=['GET'])
def hello(name):
    user = name if name else "Stranger"
    
    # Unified response format
    return success_response(
        data={"user": user},
        message="Greeting generated successfully"
    )