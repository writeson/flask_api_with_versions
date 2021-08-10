from .payment import PaymentProcessorCreator        
from app.models import db_session_manager, Merchant

def payment(version: str="", merchant_id: int=0, payload: str=""):
    """Process the payment using a factory to create the correct
    version of the payment processor

    Args:
        version (str, optional): The version string, ie: "v1". Defaults to "".
        merchant_id (int, optional): The merchant id value. Defaults to -1.
        payload (str, optional): The XML payload string. Defaults to "".

    Returns:
        dict: response structure for API
    """
    # get the correct version of the payment processor
    payment_processor_creator = PaymentProcessorCreator()
    payment_processor = payment_processor_creator.get(version)
    return payment_processor.make_payment(
        merchant_id=merchant_id, 
        payload=payload
    )
