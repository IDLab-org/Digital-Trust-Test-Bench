from flask import Blueprint

bp = Blueprint("modules", __name__)

from app.routes.modules import routes
