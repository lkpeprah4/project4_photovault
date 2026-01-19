

from flask import Flask
from .extensions import db, bcrypt, jwt, limiter, cache
 
def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

  
    from .routes.auth_routes import auth_bp
    from .routes.photo_routes import photo_bp
    from .routes.albums_routes import album_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(photo_bp)
    app.register_blueprint(album_bp)
    
        # DEBUG: print all registered routes
    print("\n[DEBUG] Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule} -> {rule.endpoint}")
    print("[END DEBUG]\n")


    return app
