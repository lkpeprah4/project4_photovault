from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import cloudinary
import cloudinary.uploader
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    cloudinary.config(
        cloud_name=app.config["CLOUDINARY_CLOUD_NAME"],
        api_key=app.config["CLOUDINARY_API_KEY"],
        api_secret=app.config["CLOUDINARY_API_SECRET"]
    )

    with app.app_context():
        db.create_all()

    from app.routes.auth_routes import auth_bp
    from app.routes.add_photo import photo_bp
    from app.routes.albums_routes import album_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(photo_bp, url_prefix="/photos")
    app.register_blueprint(album_bp, url_prefix="/albums")

    return app
