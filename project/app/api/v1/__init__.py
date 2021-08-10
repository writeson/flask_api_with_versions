from flask import Blueprint

v1_bp = Blueprint("v1_bp", __name__, url_prefix="/v1")

from . import v1