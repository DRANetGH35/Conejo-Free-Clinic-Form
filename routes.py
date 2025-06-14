import csv
import os
import sqlite3
from functools import wraps

from flask import Flask, abort, render_template, redirect, url_for, flash, request, send_file
from flask import current_app as app
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from sqlalchemy import Integer, String, Text, select, Boolean, create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from data import cities_in_california, languages
import socket
from forms import LoginForm, SubmissionForm, ChangePasswordForm, CreateNewUserForm
from graphs import render_city_of_residence_plot
import pandas as pd
import matplotlib.pyplot as plt

from extensions import db
from models import Entry, User
from app import create_app

app = create_app()


def is_logged_in():
    if current_user.is_authenticated:
        return True
    return False

#Returns True if there are any registered users (Only the admin user should exist)
def admin_user_exists():
    user = db.session.execute(db.select(User).where(User.name == 'admin')).scalar()
    if user:
        return True
    return False

# creates the admin user
def create_admin_user():
    db.session.add(User(name='admin', password=generate_password_hash('password', method="pbkdf2:sha256", salt_length=8), is_admin=True))
    db.session.commit()

# Returns true if the database exists
def database_exists():
    if os.path.exists('/instance/users.db'):
        return True
    return False

# Creates database():
def create_database():
    with app.app_context():
        db.create_all()

def user_exists(username):
    try:
        if db.session.execute(db.select(User).where(User.name == username)).scalar():
            return True
    except AttributeError:
        return False

def logged_in_as_admin():
    return is_logged_in() and current_user.is_admin == True

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #If id is not 1 then return abort with 403 error
        if not logged_in_as_admin():
            return abort(403)
        #Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET', 'POST'])
def home():
    if not admin_user_exists():
        create_admin_user()

    form = LoginForm(stored_password=db.session.execute(db.select(User).where(User.name == 'admin')).scalar().password)
    if request.method == 'GET':
        return render_template("index.html", form=form, current_user=current_user)
    if not form.validate():
        return render_template('index.html', form=form, errors=form.errors, current_user=current_user)
    login_user(db.session.execute(db.select(User).where(User.name == 'admin')).scalar())
    if form.change_password.data:
        return redirect(url_for('change_password'))
    return redirect(url_for('form'))

@app.route('/form', methods=['GET', 'POST'])
@login_required
def form():
    form = SubmissionForm()
    if request.method == 'GET':
        return render_template('form_page.html', form=form, current_user=current_user, cities_in_california=cities_in_california(), languages=languages())
    if not form.validate():
        for error in form.errors:
            flash(error)
        return render_template('form_page.html', errors=form.errors, form=form, current_user=current_user, cities_in_california=cities_in_california(), languages=languages())
    new_entry = Entry(age=form.age.data,
                      city_of_residence=form.city_of_residence.data,
                      zipcode=form.zipcode.data,
                      referred_by=form.referred_by.data,
                      education=form.education.data,
                      gender=form.gender.data,
                      ethnicity=form.ethnicity.data,
                      race=form.race.data,
                      housing=form.housing.data,
                      household_income=form.household_income.data,
                      number_of_dependants=form.number_of_dependants.data,
                      language=form.language.data,
                      employment=form.employment.data,
                      health_coverage=form.health_coverage.data,
                      hiv_status=form.hiv_status.data,
                      lgbtq_status=form.lgbtq_status.data,
                      veteran=form.veteran.data
                      )
    db.session.add(new_entry)
    db.session.commit()
    logout_user()
    return render_template('success.html')

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if request.method == 'GET':
        return render_template('change_password.html', form=form, current_user=current_user,)
    if not form.validate():
        return render_template('change_password.html', form=form, errors=form.errors, current_user=current_user,)
    if form.password.data != form.confirm_password.data:
        flash('Passwords do not match')
        return render_template('change_password.html', form=form, errors=form.errors, current_user=current_user,)
    user = db.session.execute(db.select(User).where(User.name == 'admin')).scalar()
    user.password = generate_password_hash(password=form.password.data, method='pbkdf2:sha256', salt_length=8)
    db.session.commit()
    flash('Your password has been changed')
    return redirect(url_for('home'))

@app.route('/create_new_user', methods=['GET', 'POST'])
@admin_only
def create_new_user():
    form = CreateNewUserForm()
    if request.method == 'GET':
        return render_template('create_new_user.html', form=form, current_user=current_user,)
    if not form.validate():
        return render_template('create_new_user.html', form=form, current_user=current_user, errors=form.errors)

    new_user = User(name=form.username.data,
                    password=generate_password_hash(password=form.password.data, method='pbkdf2:sha256', salt_length=8),
                    is_admin=form.is_admin.data)

    db.session.add(new_user)
    db.session.commit()
    print(f"new user: {form.username.data}\n{form.password.data}\n{form.is_admin.data}")

    return redirect(url_for('home'))

@app.route("/profile/<int:id>")
def profile(id):
    user = db.session.execute(db.select(User).where(User.id == id)).scalar()
    return render_template('profile.html', user_profile=user)

@app.route('/statistics')
@admin_only
def statistics():
    query = "SELECT * FROM entry"
    df = pd.read_sql(query, db.engine)
    df.to_excel('instance/db.xlsx', index=True)
    render_city_of_residence_plot()
    return render_template('statistics.html', current_user=current_user,)

@app.route('/dl_to_excel')
def dl_to_excel():
    return redirect(url_for('statistics'))

@app.route('/reset', methods=['GET'])
def reset():
    user = db.session.execute(db.select(User).where(User.name == 'admin')).scalar()
    user.password = generate_password_hash(password='password', method='pbkdf2:sha256', salt_length=8)
    db.session.commit()
    flash("Your password has been reset")
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    form = LoginForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', form=form, errors=form.errors, current_user=current_user,)
        if not user_exists(form.username.data):
            flash('Incorrect username or password')
            return redirect(url_for('login_route'))
        user = db.session.execute(db.select(User).where(User.name == form.username.data)).scalar()
        if not check_password_hash(user.password, form.password.data):
            flash('Incorrect username or password')
            return redirect(url_for('login_route'))
        login_user(user)
        return redirect(url_for('home'))
    else:
        return render_template('login.html', form=form, errors=form.errors, current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/test')
def test():
    print(languages())
    return redirect(url_for('home'))




if not database_exists():
    create_database()


