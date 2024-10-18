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
        
    
        

class Farmer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstnames = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())

    def __init__(self, firstnames, surname, gender, phone, address, created_at):
        self.firstnames=firstnames
        self.surname=surname
        self.gender=gender
        self.phone=phone
        self.address=address
        self.created_at = created_at

    @property
    def full_name(self):
        return f"{self.firstnames} {self.surname}"


class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())
    end_date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())

    def __init__(self, name, start_date, end_date):
        self.name=name
        self.start_date = start_date
        self.end_date = end_date



class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    farmer_id = db.Column(db.Integer, nullable=False)
    season_id = db.Column(db.Integer, nullable=False)
    stage = db.Column(db.String(80), nullable=False)
    size = db.Column(db.String(80), nullable=False)
    qty = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(80), nullable=True)
    date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())

    def __init__(self, user_id, farmer_id, season_id, stage, size, qty, name, date, created_at):
        self.user_id=user_id
        self.farmer_id=farmer_id
        self.season_id=season_id
        self.stage=stage
        self.size=size
        self.qty=qty
        self.name=name
        self.date=date
        self.created_at = created_at
        
class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    farmer_id = db.Column(db.Integer, nullable=False)
    season_id = db.Column(db.Integer, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(precision=10, scale=2))
    total_price = db.Column(db.Numeric(precision=10, scale=2))
    date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())

    def __init__(self, user_id, farmer_id, season_id, qty, unit_price, total_price, date, created_at):
        self.user_id=user_id
        self.farmer_id=farmer_id
        self.season_id=season_id
        self.qty=qty
        self.unit_price=unit_price
        self.total_price=total_price
        self.date=date
        self.created_at = created_at