from abc import ABC, abstractmethod
from app.models import (
    db_session_manager, 
    Merchant, 
    PaymentManagement, 
    Patient, 
    Payment
)
from xmltodict3 import XmlTextToDict
from flask import abort, Response
import requests
import json
from typing import Dict
from logging import getLogger

logger = getLogger(__name__)


class PaymentProcessor(ABC):
    """Abstract base class of the payment system

    Args:
        ABC (class): Abstract Base Class class
    """
    @abstractmethod
    def make_payment(self, merchant_id: int , payload: str):
        """makes a payment to the merchant"""


class PaymentProcessorV1(PaymentProcessor):
    """Version 1 of the payment system
    * NOTE * This version does not requires a payment note

    Args:
        ABC (class): Abstract Base Class class
    """
    def __init__(self):
        logger.info("Created Payment Processor V1")
        
    def make_payment(self, merchant_id: int , payload: str):
        with db_session_manager() as db_session:
            merchant = get_merchant(db_session, merchant_id)
            
            # get the payment processor
            payment_manager_creator = PaymentManagerCreator()
            payment_manager = payment_manager_creator.get(merchant.payment_management.name)
            if payment_manager is None:
                abort(Response(f"Payment management: {merchant.payment_management.name} not found", status=400))

            # parse the xml payload
            payment_data = parse_payload(payload)

            # call the merchant payment manager and make a payment
            url = merchant.payment_management_url
            payment_manager.post_payment(url, payment_data)

            # update the database with payment information
            # *NOTE* I'd clean this up and validate the payload
            first_name = payment_data.get("payment", {}).get("patient", {}).get("first_name")
            last_name = payment_data.get("payment", {}).get("patient", {}).get("last_name")
            amount = payment_data.get("payment", {}).get("amount")
            patient = (
                db_session.query(Patient)
                .filter(Patient.first_name == first_name)
                .filter(Patient.last_name == last_name)
                .one_or_none()
            )
            # is this a new patient?
            if patient is None:
                patient = Patient(
                    first_name=first_name,
                    last_name=last_name
                )
                # add the new patient to the merchant
                merchant.patients.append(patient)

            # add the payment to the patients records
            patient.payments.append(
                Payment(amount=amount)
            )
            # update the merchant and save to the database
            db_session.add(merchant)
            db_session.commit()

        return "success"


class PaymentProcessorV2(PaymentProcessor):
    """Version 2 of the payment system
    * NOTE * This version requires a payment note

    Args:
        ABC (class): Abstract Base Class class
    """
    def __init__(self):
        logger.info("Created Payment Processor V2")
        
    def make_payment(self, merchant_id: int , payload: str):
        with db_session_manager() as db_session:
            merchant = get_merchant(db_session, merchant_id)
            
            # get the payment processor
            payment_manager_creator = PaymentManagerCreator()
            payment_manager = payment_manager_creator.get(merchant.payment_management.name)
            if payment_manager is None:
                abort(Response(f"Payment management: {merchant.payment_management.name} not found", status=400))

            # parse the xml payload
            payment_data = parse_payload(payload)

            # call the merchant payment manager and make a payment
            url = merchant.payment_management_url
            payment_manager.post_payment(url, payment_data)

            # update the database with payment information
            # *NOTE* I'd clean this up and validate the payload
            first_name = payment_data.get("payment", {}).get("patient", {}).get("first_name")
            last_name = payment_data.get("payment", {}).get("patient", {}).get("last_name")
            amount = payment_data.get("payment", {}).get("amount")
            # this is the difference between V1 and V2, a note is required
            note = payment_data.get("payment", {}).get("note")
            patient = (
                db_session.query(Patient)
                .filter(Patient.first_name == first_name)
                .filter(Patient.last_name == last_name)
                .one_or_none()
            )
            # is this a new patient?
            if patient is None:
                patient = Patient(
                    first_name=first_name,
                    last_name=last_name
                )
                # add the new patient to the merchant
                merchant.patients.append(patient)

            # add the payment to the patients records
            patient.payments.append(
                Payment(amount=amount)
            )
            # update the merchant and save to the database
            db_session.add(merchant)
            db_session.commit()               

        return "success"


class PaymentProcessorFactory(ABC):
    """A Payment Factory interface

    Args:
        ABC (clss): Abstract base class
    """
    def get(self, version: str) -> PaymentProcessor:
        """Returns a new payment instance"""


class PaymentProcessorCreator(PaymentProcessorFactory):
    """A Payment creator that actually returns instances
    of a payment object

    Args:
        PaymentFactory (class): PaymentFactory
    """
    PAYMENT_VERSIONS = {
        "v1": PaymentProcessorV1,
        "v2": PaymentProcessorV2,
    }
    def get(self, version: str) -> PaymentProcessor:
        payment_processor_class = PaymentProcessorCreator.PAYMENT_VERSIONS.get(version)
        return payment_processor_class()


class PaymentManager(ABC):
    """Abstract base class of the payment manager system

    Args:
        ABC (class): Abstract Base Class class
    """
    @abstractmethod
    def post_payment(self, payment_data: Dict):
        """post a payment to the payment manager"""


class EagleSoftPaymentManager(PaymentManager):
    """Version 1 of the Eaglesoft merchant system

    Args:
        ABC (class): Abstract Base Class class
    """
    def __init__(self):
        logger.info("Created EagleSoft Payment Manager")

    def post_payment(self, url: str, payment_data: Dict):
        # here I'd use the requests module to make the HTTP request
        # to the payment manager using the passed in URL
        first_name = payment_data.get("payment", {}).get("patient", {}).get("first_name")
        last_name = payment_data.get("payment", {}).get("patient", {}).get("last_name")
        amount = payment_data.get("payment", {}).get("amount")
        logger.info((
            f"Posting payment to {url=} "
            f"for {first_name} {last_name} in the amount of "
            f"{amount}"
        ))


class WhoKnowsWhatPaymentManager(PaymentManager):
    """Version 2 of the Who Knows What merchant system

    Args:
        ABC (class): Abstract Base Class class
    """
    def __init__(self):
        logger.info("Created Who Knows What Payment Manager")
        
    def post_payment(self, url: str, payment_data: Dict):
        # here I'd use the requests module to make the HTTP request
        # to the payment manager using the passed in URL
        first_name = payment_data.get("payment", {}).get("patient", {}).get("first_name")
        last_name = payment_data.get("payment", {}).get("patient", {}).get("last_name")
        amount = payment_data.get("payment", {}).get("amount")
        logger.info((
            f"Posting payment to {url=} "
            f"for {first_name} {last_name} in the amount of "
            f"{amount}"
        ))


class PaymentManagerFactory(ABC):
    """A Merchant Processor Factory interface

    Args:
        ABC (clss): Abstract base class
    """
    def get(self, merchant_name: str) -> Merchant:
        """Returns a new payment instance"""


class PaymentManagerCreator(PaymentManagerFactory):
    """A Merchant creator that actually returns instances
    of a merchant object

    Args:
        MerchantFactory (class): MerchantFactory
    """
    PAYMENT_MANAGERS = {
        "eaglesoft": EagleSoftPaymentManager,
        "whoknowswhat": WhoKnowsWhatPaymentManager,
    }
    def get(self, merchant_name: str) -> Merchant:
        payment_manager_class = PaymentManagerCreator.PAYMENT_MANAGERS.get(merchant_name.lower())
        return payment_manager_class()


def get_merchant(db_session, merchant_id: int) -> Merchant:
    return (
        db_session.query(Merchant)
        .filter(Merchant.merchant_id == merchant_id)
        .filter(Merchant.active == True)
        .one_or_none()
    )


def parse_payload(payload: str):
    """This function parses the XML payload into a
    data structure

    Args:
        payload (str): XML payload string
    """
    return XmlTextToDict(payload, ignore_namespace=True).get_dict()
    