from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, IntegerField, SelectField, DateField, DateTimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Regexp, Optional
from wtforms_sqlalchemy.fields import QuerySelectField
from models import User, Farmer, Season 
import datetime


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')
    

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    

class UserForm(FlaskForm):
    role_choices = [(2, 'Field Officer'),
               (1, 'Admin')]
    role = SelectField('Select Role', choices=role_choices, validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
     

class SeasonForm(FlaskForm):
    name = StringField('Season Name', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')


zimbabwe_phone_regex = r'^07\d{8}$'

class FarmerForm(FlaskForm):
    firstnames = StringField('First Names', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    phone = StringField('Phone Number (without country code)', validators=[
        DataRequired(), 
        Regexp(zimbabwe_phone_regex, message="Phone number must be a valid Zimbabwe mobile number")
    ])
    address = StringField('Address', validators=[DataRequired()])
    
    submit = SubmitField('Submit')     

class RecordForm(FlaskForm):
    stage_choices = [('PLANTING', 'PLANTING'),
               ('FERTILATION', 'FERTILIZATION'),
               ('PEST CONTROL', 'PEST CONTROL'),
               ('HARVEST', 'HARVEST')]
    farmer_id = QuerySelectField('Select Farmer', query_factory=lambda: Farmer.query.all(), get_label="full_name", allow_blank=False, validators=[DataRequired()])
    season_id = QuerySelectField('Select Season', query_factory=lambda: Season.query.all(), get_label="name", allow_blank=False, validators=[DataRequired()])
    stage = SelectField('Select Farming Stage', choices=stage_choices, validators=[DataRequired(), Length(max=80)])
    size = StringField('Field Size', validators=[DataRequired(), Length(max=80)])
    qty = IntegerField('Quantity (kgs/litres) (optinal)', validators=[Optional()])
    name = StringField('Name (chemicals/fertilizers) (optinal)', validators=[Optional(), Length(max=80)])
    
    submit = SubmitField('Save Record')
    
    
class SaleForm(FlaskForm):
    farmer_id = QuerySelectField('Select Farmer', query_factory=lambda: Farmer.query.all(), get_label="full_name", allow_blank=False, validators=[DataRequired()])
    season_id = QuerySelectField('Select Season', query_factory=lambda: Season.query.all(), get_label="name", allow_blank=False, validators=[DataRequired()])
    qty = IntegerField('Quantity (KGs)', validators=[DataRequired()])
    unit_price = DecimalField('Unit Price', places=2, validators=[DataRequired()])
    
    submit = SubmitField('Save Sale')