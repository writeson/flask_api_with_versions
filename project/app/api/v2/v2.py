from flask import request, jsonify
from logging import getLogger
from . import v2_bp
from ..common.handler import payment

logger = getLogger(__file__)


@v2_bp.get("/")
def home():
    logger.debug("rendering the V2 home page")
    return "Welcome to the V2 home page"


@v2_bp.post("/<int:merchant_id>/payment")
def post(merchant_id):
    return jsonify(payment(
        version="v2", 
        merchant_id=merchant_id, 
        payload=request.data
    ))