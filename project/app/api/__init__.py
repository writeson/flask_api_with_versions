from flask import Blueprint
from .v1 import v1_bp
from .v2 import v2_bp

api_bp = Blueprint("api_bp", __name__, url_prefix="/api")

# register the version apis on the parent
api_bp.register_blueprint(v1_bp)
api_bp.register_blueprint(v2_bp)

from app.api import api

