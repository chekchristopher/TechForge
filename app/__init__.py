from flask import Flask

from config import Config
from app.extensions import db, migrate, cors


def create_app(config_class=Config):

    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    cors(
        app,
        resources={
            r"/api/*": {
                "origins": "*"
            }
        }
    )

    from app.routes.programme_routes import programme_bp
    from app.routes.trainee_routes import trainee_bp
    from app.routes.registration_routes import registration_bp

    app.register_blueprint(programme_bp)
    app.register_blueprint(trainee_bp)
    app.register_blueprint(registration_bp)

    @app.get("/api/health")
    def health_check():
        return {
            "success": True,
            "message": "TechForge API is running"
        }

    return app