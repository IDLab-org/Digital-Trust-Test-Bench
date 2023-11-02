from flask import Flask, session
from flask_cors import CORS
from config import Config
import logging

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    if __name__ != "__main__":
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    from app.errors import bp as errors_bp

    app.register_blueprint(errors_bp)

    from app.routes.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.routes.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.routes.test_suites import bp as test_suites_bp

    app.register_blueprint(test_suites_bp, url_prefix="/test-suites")

    return app
