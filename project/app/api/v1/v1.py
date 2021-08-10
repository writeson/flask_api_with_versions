from flask import request, jsonify
from logging import getLogger
from . import v1_bp
from ..common.handler import payment

logger = getLogger(__file__)


@v1_bp.get("/")
def home():
    logger.debug("rendering the V1 home page")
    return "Welcome to the V1 home page"


@v1_bp.post("/<int:merchant_id>/payment")
def post(merchant_id):
    return jsonify(payment(
        version="v1", 
        merchant_id=merchant_id, 
        payload=request.data
    ))
