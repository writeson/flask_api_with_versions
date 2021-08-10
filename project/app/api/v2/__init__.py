from flask import Blueprint

v2_bp = Blueprint("v2_bp", __name__, url_prefix="/v2")

from . import v2