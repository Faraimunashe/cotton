from flask import Flask, jsonify, request, redirect, render_template, url_for, flash, session,wrappers, make_response
from flask_session import Session
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os
from models import *
from functools import wraps
from forms import LoginForm, RegistrationForm, LoanForm
from passlib.hash import sha256_crypt
import pandas as pd
import pdfkit



app = Flask(__name__)
app.config['SECRET_KEY'] = 'ProfessorSecret'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/loan_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cotton.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

def admin_role(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        user = User.query.filter_by(id=session['userid']).first()
        if user.role == 1:
            return f(*args, **kwargs)
        else:
            return redirect("/")
    return decorated_func

@app.route('/', methods=['GET', 'POST'])
def index():
    
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('error Invalid login details.')
            return redirect(url_for('login'))
        if sha256_crypt.verify(password, user.password):
            login_user(user)
            session['userid'] = user.id
            return redirect(url_for('dashboard'))

        flash('error Invalid login details.')
        return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        passwordata = sha256_crypt.encrypt(password)

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Error email already exists!')
            return redirect(url_for('register'))
        new_user = User(email=email, password=passwordata, name=name, role=1)
        db.session.add(new_user)
        db.session.commit()

        flash('Successfully registered new user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    admins = User.query.filter_by(role=1).count()
    officers = User.query.filter_by(role=2).count()
    farmers = User.query.filter_by(role=3).count()
    return render_template('dashboard.html', admins=admins, officers=officers, farmers=farmers)


@app.route('/admin-dashboard', methods=['GET', 'POST'])
@login_required
@admin_role
def admin_dashboard():
    
    return render_template('admin_dashboard.html')


@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/loan-transactions', methods=['GET'])
@login_required
@admin_role
def loan_transactions():
    loan_applications = db.session.query(LoanApplication, User).join(User, LoanApplication.user_id == User.id).all()
    return render_template('loan_transactions.html', loan_applications=loan_applications)


@app.route('/generate_pdf', methods=['GET'])
def generate_pdf():
    loan_applications = db.session.query(LoanApplication, User).join(User, LoanApplication.user_id == User.id).all()
    html = render_template('pdf_template.html', loan_applications=loan_applications)
    pdf = pdfkit.from_string(html, False, configuration=config)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
    return response


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    g=None
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
