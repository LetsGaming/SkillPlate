import importlib
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

from utils.logger import LOGGER
from utils.utils import ROOT_DIR, load_config


def load_debug():
    config = load_config()
    debug = config.get("debug", False)
    return debug

def load_port():
    config = load_config()
    server_config = config.get("server", {})
    port = server_config.get("port", 5000)
    return port

def create_app():
    app = Flask(__name__)

    CORS(app)

    # Dynamically import and register API blueprints
    api_directory = "api"
    not_allowed_names = ["__init__.py", "config.py"]

    api_path = os.path.join(ROOT_DIR, api_directory)
    api_files = [
        file[:-3]
        for file in os.listdir(api_path)
        if file.endswith(".py") and file not in not_allowed_names
    ]

    for api_file in api_files:
        module = importlib.import_module(f"{api_directory}.{api_file}")
        blueprint = getattr(module, f"{api_file}_api")
        app.register_blueprint(blueprint)

    return app

app = create_app()

@app.route('/api/hello', defaults={'name': None}, methods=['GET'])
@app.route('/api/hello/<string:name>', methods=['GET'])
def hello(name):
    user = name if name else "Stranger"
    return jsonify(message=f"Hello, {user}!")

if __name__ == '__main__':
    port = load_port()
    debug = load_debug()
    LOGGER.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', debug=debug, port=port)
