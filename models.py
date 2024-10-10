from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime

db = SQLAlchemy()

#from .models import User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    role = db.Column(db.Integer)

    def __init__(self, email, password, name, role):
        self.email=email
        self.password=password
        self.name=name
        self.role=role

class LoanApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    married = db.Column(db.String(20), nullable=False)
    dependents = db.Column(db.String(20), nullable=False)
    education = db.Column(db.String(20), nullable=False)
    self_employed = db.Column(db.String(20), nullable=False)
    application_income = db.Column(db.String(20), nullable=False)
    coapplication_income = db.Column(db.String(20), nullable=False)
    loan_amount = db.Column(db.String(20), nullable=False)
    loan_amount_term = db.Column(db.String(20), nullable=False)
    credit_history = db.Column(db.String(20), nullable=False)
    property_area = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())

    def __init__(self, user_id, gender, married, dependents, education, self_employed, application_income, coapplication_income, loan_amount, loan_amount_term, credit_history, property_area, status, created_at):
        self.user_id = user_id
        self.gender = gender
        self.married = married
        self.dependents = dependents
        self.education = education
        self.self_employed = self_employed
        self.application_income=application_income
        self.coapplication_income=application_income
        self.loan_amount = loan_amount
        self.loan_amount_term = loan_amount_term
        self.credit_history = credit_history
        self.property_area = property_area
        self.status = status
        self.created_at = created_at
