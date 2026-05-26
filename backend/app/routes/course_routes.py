from flask import Blueprint

from app.services.ollama_service import generate_course_content
from app.utils.responses import success_response

course_routes = Blueprint("course_routes", __name__, url_prefix="/course")

@course_routes.route('/', defaults={'id': None}, methods=['GET'])
@course_routes.route('/<string:id>', methods=['GET'])
def get_course(id):
    return success_response(
        data={"courseId": id},
        message="Course fetched successfully")


@course_routes.route('/', defaults={'theme': None, 'difficulty': None, 'duration': None, 'online': None}, methods=['POST'])
@course_routes.route('/<string:theme>/<string:difficulty>/<int:duration>/<string:online>', methods=['POST'])
def create_course(theme, difficulty, duration, online):
    online_bool = online.lower() in ("true", "1", "yes") if online else None
    
    course = generate_course_content(theme, difficulty, duration, online_bool)
    return success_response(
        data={"course": course},
        message="Course created successfully")