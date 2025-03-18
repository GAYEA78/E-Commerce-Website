import os

from flask.cli import load_dotenv

from app import create_app

load_dotenv()

config_name = os.getenv("FLASK_ENV", "development")

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    debug = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "t")
    app.run(host="0.0.0.0", port=port, debug=debug)
