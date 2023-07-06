import os

from dotenv import load_dotenv
from flask import Flask


def create_app() -> Flask:
    load_dotenv()

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

    with app.app_context():
        from app.blueprints import register_blueprints

        register_blueprints(app)

        from app.database import automigrate

        automigrate()

        return app
