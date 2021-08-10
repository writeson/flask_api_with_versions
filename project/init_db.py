# this just initializes the database with some data

import os
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from app import create_app
from app.models import (
    db_session_manager, 
    Patient,
    Payment,
    Merchant, 
    PaymentManagement
)

# delete the existing database file if it exists
filepath = Path(__file__).parent / "app" / "rectangle.sqlite"
if filepath.exists():
    os.remove(filepath)

# create database
# app = Flask(__name__)
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(filepath)
# db.create_all()
app = create_app()

with app.app_context():
    # put data in the database
    with db_session_manager() as db_session:
        patient_1 = Patient(
            first_name="George",
            last_name="Schultz",
            payments=[
                Payment(amount=127.47, note="Paid in Full"),
                Payment(amount=35.16, note="Insurance")
            ]
        )
        patient_2 = Patient(
            first_name="Samuel",
            last_name="Adams",
            payments=[
                Payment(amount=15.83, note="Partial Payment")
            ]
        )
        merchant_1 = Merchant(
            name="East Coast Merchant",
            payment_management_url="https://east_coast_eaglesoft.com/api/payment",
            payment_management=PaymentManagement(name="EagleSoft"),
            patients=[patient_1]
        )
        
        merchant_2 = Merchant(
            name="Midwest Merchant",
            payment_management_url="https://midwest_who_knows_what.com/api/payment",
            payment_management=PaymentManagement(name="WhoKnowsWhat"),
            patients=[patient_2]
        )
        db_session.add(merchant_1)
        db_session.add(merchant_2)
        db_session.commit()
