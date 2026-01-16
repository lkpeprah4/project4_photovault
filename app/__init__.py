from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.routes.auth_routes import auth_bp


db=SQLAlchemy()
jwt=JWTManager()
bcrypt=Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.register_blueprint(auth_bp)


    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    return app