from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # Register Blueprints
    from app.routes.main_routes import main_bp
    app.register_blueprint(main_bp)

    # Create tables in the database
    with app.app_context():
        db.create_all()

    return app
