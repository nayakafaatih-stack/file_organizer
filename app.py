from flask import Flask
from dotenv import load_dotenv

from app.routes.home import home_bp
from app.routes.preview import preview_bp
from app.routes.organize import organize_bp

import os

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DEBUG"] = os.getenv("DEBUG") == "True"

app.register_blueprint(home_bp)
app.register_blueprint(preview_bp)
app.register_blueprint(organize_bp)

if __name__ == "__main__":
    app.run()