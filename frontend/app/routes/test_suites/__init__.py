from flask import Blueprint

bp = Blueprint("test_suites", __name__)

from app.routes.test_suites import routes
