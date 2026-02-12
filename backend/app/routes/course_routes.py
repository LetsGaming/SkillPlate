from flask import Blueprint

from backend.app.services.ollama_service import generate_course_content
from backend.app.utils.responses import success_response

course_routes = Blueprint("course_routes", __name__)


@course_routes.route('/course', defaults={'id': None}, methods=['GET'])
@course_routes.route('/course/<string:id>', methods=['GET'])
def get_course(id):
    return success_response(
        data={"courseId": id},
        message="Course fetched successfully")


@course_routes.route('/course', defaults={'theme': None, 'difficulty': None, 'duration': None, 'online': None},
                     methods=['POST'])
@course_routes.route('/course/<string:theme>/<string:difficulty>/<string:duration>/<string:online>', methods=['POST'])
def create_course(theme, difficulty, duration, online):
    course = generate_course_content(theme, difficulty, duration, online)
    return success_response(
        message="Course created successfully")
