import os
import sys

# We use a relative import because run.py is now inside the 'app' package
from . import create_app

app = create_app()

if __name__ == '__main__':
    # 1. Configuration Check
    # We pull from app.config first (populated by config.py), 
    # then fallback to environment variables
    port = app.config.get("PORT", int(os.getenv("PORT", 5000)))
    debug = app.config.get("DEBUG", os.getenv("DEBUG", "false").lower() in ("1", "true", "yes"))
    
    # Using your identity for the startup log
    author = app.config.get("AUTHOR", {"name": "LetsGamingDE"})
    print(f"--- Server Starting ---")
    print(f"Author: {author['name']}")
    print(f"Port:   {port}")
    print(f"Debug:  {debug}")
    print(f"-----------------------")

    app.run(host='0.0.0.0', debug=debug, port=port)