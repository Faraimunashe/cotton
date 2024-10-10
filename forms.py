from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange


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
     


class LoanForm(FlaskForm):
    edu_choices = [('Not Graduate', 'Not Graduate'),('Graduate', 'Graduate')]
    gender_choices = [('Male', 'Male'),('Female', 'Female')]
    married_choices = [('Yes', 'Yes'),('No', 'No')]
    employment_choices = [('Yes', 'Yes'),('No', 'No')]
    credit_choices = [(0, '0'),(1, '1')]
    property_choices = [('Rural', 'Rural'),('Semiurban', 'Semiurban'),('Urban', 'Urban')]
    
    gender = SelectField('Gender', choices=gender_choices)
    married = SelectField('Married', choices=married_choices)
    dependents = DecimalField('Dependents', validators=[DataRequired(), NumberRange(min=1, max=10)])
    education = SelectField('Education', choices=edu_choices)
    self_employed = SelectField('Self Employeed', choices=employment_choices)
    application_income = DecimalField('Application Income', validators=[DataRequired(), NumberRange(min=0.01)])
    coapplication_income = DecimalField('Coapplication Income', validators=[DataRequired(), NumberRange(min=0.01)])
    loan_amount = DecimalField('Loan Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    loan_amount_term = DecimalField('Loan Amount Term', validators=[DataRequired(), NumberRange(min=1)])
    credit_history = SelectField('Credit History', choices=credit_choices)
    property_area = SelectField('Property Area', choices=property_choices)
    
    submit = SubmitField('Apply Loan')