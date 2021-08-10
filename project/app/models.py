from contextlib import contextmanager
from . import db
from datetime import datetime


@contextmanager
def db_session_manager():
    """This is a Flask SQLAlchemy session context manager
    This does the right thing no matter how the context
    is exited

    Yields:
        [type]: [description]
    """
    try:
        yield db.session
    except Exception as e:
        db.session.rollback()
        raise
    finally:
        db.session.close()


class Patient(db.Model):
    __tablename__ = "patient"
    patient_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)        
    merchant_id = db.Column(db.Integer, db.ForeignKey("merchant.merchant_id"), nullable=False)
    payments = db.relationship("Payment", backref=db.backref("patient"))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = db.Column(db.Boolean, nullable=False, default=True)


class Payment(db.Model):
    __tablename__ = "payment"
    payment_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.patient_id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    note = db.Column(db.String, default="NA")
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Merchant(db.Model):
    """This is the merchant class that maps the merchant data in the system

    Args:
        db (object): The Flask SQLAlchemy db model class
    """
    __tablename__ = "merchant"
    merchant_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, index=True)
    payment_management_id = db.Column(db.Integer, db.ForeignKey("payment_management.payment_management_id"), nullable=False)
    payment_management_url = db.Column(db.String, nullable=False)
    patients = db.relationship("Patient", backref=db.backref("merchant"))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = db.Column(db.Boolean, nullable=False, default=True)


class PaymentManagement(db.Model):
    """This is the payment manage class the maps the payment management data in the system

    Args:
        db (object): The Flask SQLAlchemy db model class
    """
    __tablename__ = "payment_management"
    payment_management_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, index=True)
    merchants = db.relationship("Merchant", backref=db.backref("payment_management", uselist=False, lazy="joined"))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = db.Column(db.Boolean, nullable=False, default=True)
