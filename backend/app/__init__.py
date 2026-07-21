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
    CORS(app, supports_credentials=True, origins=app.config.get("CORS_ORIGINS", ["http://localhost:5173"]))
    jwt.init_app(app)
    
    # Register the custom error responses for JWT
    register_jwt_callbacks(jwt)

    # --- Global Exception Handler ---
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return error_response(e.description, e.code)
        
        LOGGER.error(f"Unhandled Exception: {str(e)}", exc_info=True)
        return error_response("An internal server error occurred", 500)

    # --- Dynamic Blueprint Loader ---
    base_dir = os.path.dirname(os.path.abspath(__file__))
    routes_path = os.path.join(base_dir, "routes")

    if os.path.exists(routes_path):
        for file in os.listdir(routes_path):
            if file.endswith(".py") and file != "__init__.py":
                module_name = file[:-3]
                try:
                    module = importlib.import_module(f"app.routes.{module_name}")
                    
                    blueprint_attr = f"{module_name}_routes"
                    if not hasattr(module, blueprint_attr):
                        blueprint_attr = module_name
                    
                    if hasattr(module, blueprint_attr):
                        blueprint = getattr(module, blueprint_attr)

                        # Combine /api/v1 with the blueprint's own url_prefix (e.g. /auth, /course)
                        base_prefix = f"/api{Config.VERSION_PATH}"
                        bp_prefix = getattr(blueprint, "url_prefix", "") or ""
                        full_prefix = f"{base_prefix}{bp_prefix}"

                        app.register_blueprint(blueprint, url_prefix=full_prefix)
                        
                        LOGGER.info(f"Registered blueprint: {blueprint_attr} at {full_prefix}")
                    else:
                        LOGGER.warning(f"Skipping {file}: No attribute found.")
                        
                except Exception as e:
                    LOGGER.error(f"Could not load module {module_name}: {e}")

    return app