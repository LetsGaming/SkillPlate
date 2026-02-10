import os
import importlib
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException

from app.utils.logger import LOGGER
from app.config import Config
from app.utils.responses import error_response
from app.utils.jwt_callbacks import register_jwt_callbacks

# Initialize extension
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)

    # Initialize Extensions
    CORS(app)
    jwt.init_app(app)
    
    # Register the custom error responses for JWT (Fixes "not accessed" warnings)
    register_jwt_callbacks(jwt)

    # --- Global Exception Handler ---
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Handle standard Flask/Werkzeug HTTP errors (404, 405, etc.)
        if isinstance(e, HTTPException):
            return error_response(e.description, e.code)
        
        # Log unexpected Python errors
        LOGGER.error(f"Unhandled Exception: {str(e)}", exc_info=True)
        return error_response("An internal server error occurred", 500)

    # --- Dynamic Blueprint Loader ---
    base_dir = os.path.dirname(os.path.abspath(__file__))
    routes_path = os.path.join(base_dir, "routes")

    if os.path.exists(routes_path):
        for file in os.listdir(routes_path):
            # Process only .py files and ignore __init__.py
            if file.endswith(".py") and file != "__init__.py":
                module_name = file[:-3]
                try:
                    # Import the module (e.g., app.routes.system_routes)
                    module = importlib.import_module(f"app.routes.{module_name}")
                    
                    # Naming Logic: 
                    # 1. Try file_routes (e.g., if file is auth.py, look for auth_routes)
                    # 2. Try file (e.g., if file is system_routes.py, look for system_routes)
                    blueprint_attr = f"{module_name}_routes"
                    if not hasattr(module, blueprint_attr):
                        blueprint_attr = module_name
                    
                    if hasattr(module, blueprint_attr):
                        blueprint = getattr(module, blueprint_attr)
                        app.register_blueprint(blueprint)
                        LOGGER.info(f"Registered blueprint: {blueprint_attr}")
                    else:
                        LOGGER.warning(f"Skipping {file}: No attribute '{module_name}' or '{module_name}_routes' found.")
                        
                except Exception as e:
                    LOGGER.error(f"Could not load module {module_name}: {e}")

    return app