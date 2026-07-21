from flask import Blueprint

from app.utils.responses import success_response

system_routes = Blueprint("system_routes", __name__, url_prefix="/system")

@system_routes.route('/hello', defaults={'name': None}, methods=['GET'])
@system_routes.route('/hello/<string:name>', methods=['GET'])
def hello(name):
    user = name if name else "Stranger"
    
    # Unified response format
    return success_response(
        data={"user": user},
        message="Greeting generated successfully"
    )