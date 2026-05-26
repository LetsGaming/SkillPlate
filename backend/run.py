import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = app.config.get("PORT", int(os.getenv("PORT", 5000)))
    debug = app.config.get("DEBUG", os.getenv("DEBUG", "false").lower() in ("1", "true", "yes"))
    
    author = app.config.get("AUTHOR", {"name": "LetsGamingDE"})
    print(f"--- Server Starting ---")
    print(f"Author: {author['name']}")
    print(f"Port:   {port}")
    print(f"Debug:  {debug}")
    print(f"-----------------------")

    app.run(host='0.0.0.0', debug=debug, port=port)