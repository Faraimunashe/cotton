from flask import Flask, jsonify, request, redirect, render_template, url_for, flash, session,wrappers, make_response
from flask_session import Session
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os
from models import *
from functools import wraps
from forms import *
from passlib.hash import sha256_crypt
import pandas as pd
import pdfkit
import time

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


@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    form = UserForm()
    if form.validate_on_submit():
        print("here ...")
        name = form.name.data
        email = form.email.data
        password = form.password.data
        passwordata = sha256_crypt.encrypt(password)

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Error email already exists!')
            return redirect(url_for('users'))
        new_user = User(email=email, password=passwordata, name=name, role=1)
        db.session.add(new_user)
        db.session.commit()

        flash('Successfully registered new user!')
        return redirect(url_for('users'))
    users = User.query.all()
    return render_template('users.html', form=form, users=users)


@app.route('/farmers', methods=['GET', 'POST'])
@login_required
@admin_role
def farmers():
    form = FarmerForm()
    if form.validate_on_submit():
        firstnames = form.firstnames.data
        surname = form.surname.data
        gender = form.gender.data
        phone = form.phone.data
        address = form.address.data

        new_farmer = Farmer(firstnames=firstnames, surname=surname, gender=gender, phone=phone, address=address, created_at=datetime.datetime.now())
        db.session.add(new_farmer)
        db.session.commit()

        flash('Successfully registered new farmer!')
        return redirect(url_for('farmers'))
    farmers = Farmer.query.all()
    return render_template('farmers.html', form=form, farmers=farmers)


@app.route('/seasons', methods=['GET', 'POST'])
@login_required
@admin_role
def seasons():
    form = SeasonForm()
    if form.validate_on_submit():
        name = form.name.data
        start_date = form.start_date.data
        end_date = form.end_date.data

        new_season = Season(name=name, start_date=start_date, end_date=end_date)
        db.session.add(new_season)
        db.session.commit()

        flash('Successfully added new season!')
        return redirect(url_for('seasons'))
    seasons = Season.query.all()
    return render_template('seasons.html', form=form, seasons=seasons)


@app.route('/records', methods=['GET', 'POST'])
@login_required
@admin_role
def records():
    form = RecordForm()
    if form.validate_on_submit():
        user_id = session['userid']
        farmer_id = form.farmer_id.data
        season_id = form.season_id.data
        stage = form.stage.data
        size = form.size.data
        qty = form.qty.data
        name = form.name.data

        new_record = Record(user_id=user_id, farmer_id=farmer_id.id, season_id=season_id.id, stage=stage, size=size, qty=qty, name=name, date=datetime.datetime.now(), created_at=datetime.datetime.now())
        db.session.add(new_record)
        db.session.commit()

        flash('Successfully added new record!')
        return redirect(url_for('records'))
    records = db.session.query(Record.id, Record.qty, Record.name, Record.stage, Record.size, Record.date, Season.name.label('season'), Farmer.firstnames, Farmer.surname)\
        .join(Season, Record.season_id == Season.id)\
        .join(Farmer, Record.farmer_id == Farmer.id)\
        .all()
    return render_template('records.html', form=form, records=records)


@app.route('/sales', methods=['GET', 'POST'])
@login_required
@admin_role
def sales():
    form = SaleForm()
    if form.validate_on_submit():
        user_id = session['userid']
        farmer_id = form.farmer_id.data
        season_id = form.season_id.data
        qty = form.qty.data
        unit_price = form.unit_price.data
        total_price = qty * unit_price

        new_sale = Sale(user_id=user_id, farmer_id=farmer_id.id, season_id=season_id.id, qty=qty, unit_price=unit_price, total_price=total_price, date=datetime.datetime.now(), created_at=datetime.datetime.now())
        db.session.add(new_sale)
        db.session.commit()

        flash('Successfully added new sale!')
        return redirect(url_for('sales'))
    sales = db.session.query(Sale.id, Sale.qty, Sale.unit_price, Sale.total_price, Sale.date, Season.name, Farmer.firstnames, Farmer.surname)\
        .join(Season, Sale.season_id == Season.id)\
        .join(Farmer, Sale.farmer_id == Farmer.id)\
        .all()
    return render_template('sales.html', form=form, sales=sales)

def get_fraudulent_farmers(season_id):
    farmers_with_records = db.session.query(Record.farmer_id)\
                                     .filter_by(season_id=season_id)\
                                     .distinct().all()
    
    farmers_with_sales = db.session.query(Sale.farmer_id)\
                                   .filter_by(season_id=season_id)\
                                   .distinct().all()
    
    farmers_with_records_set = {farmer_id for (farmer_id,) in farmers_with_records}
    farmers_with_sales_set = {farmer_id for (farmer_id,) in farmers_with_sales}
    
    farmers_with_no_sales = farmers_with_records_set - farmers_with_sales_set
    
    
    return farmers_with_no_sales




@app.route('/frauds', methods=['GET', 'POST'])
@login_required
@admin_role
def frauds():
    frauds = []
    if request.method == "POST":
        season_id = request.form.get('season_id')
        
        frauds = get_fraudulent_farmers(season_id)
    
    return render_template('frauds.html', frauds=frauds)

@app.route('/check', methods=['GET'])
def check():
    seasons = Season.query.all()
    farmers = Farmer.query.all()
    return render_template('check.html', seasons=seasons, farmers=farmers)

@app.route('/check-fraud', methods=['POST'])
def check_fraud():
    
    farmer_id = request.json['farmer_id']
    season_id = request.json['season_id']
    
    farmers_with_no_sales = get_fraudulent_farmers(season_id)
    
    time.sleep(5)
    farmer_id = int(farmer_id)

    if farmer_id in farmers_with_no_sales:
        return jsonify({'fraud': True, 'message': 'Suspicious activity detected: No sales recorded.'})
    
    return jsonify({'fraud': False, 'message': 'No suspicious activity detected.'})


@app.route('/generate_pdf', methods=['GET'])
def generate_pdf():
    loan_applications = []
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
