from flask import jsonify
from logging import getLogger
from . import api_bp

logger = getLogger(__file__)


@api_bp.app_errorhandler(400)
@api_bp.app_errorhandler(404)
@api_bp.app_errorhandler(405)
def api_bad_request(e):
    return jsonify({
        "error": str(e)
    })


@api_bp.get("/")
def home():
    logger.debug("rendering api home page")
    return "Welcome to the API Home page"


