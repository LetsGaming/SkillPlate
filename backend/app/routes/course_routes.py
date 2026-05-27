from app.services.ollama_service import generate_course_content
from app.utils.responses import success_response
from flask import Blueprint

course_routes = Blueprint("course_routes", __name__, url_prefix="/course")


@course_routes.route('/', defaults={'id': None}, methods=['GET'])
@course_routes.route('/<string:id>', methods=['GET'])
def get_course(id):
    return success_response(
        data={"courseId": id},
        message="Course fetched successfully")


@course_routes.route('/', defaults={'theme': None, 'difficulty': None, 'duration': None, 'online': None},
                     methods=['POST'])
@course_routes.route('/<theme>/<difficulty>/<duration>/<online>', methods=['POST'])
def create_course(theme, difficulty, duration: str, online):
    duration_ = int(duration)
    online_ = bool(online)
    course = generate_course_content(theme, difficulty, duration_, online_)
    return success_response(
        data={"course": course.model_dump()},
        message="Course created successfully")
