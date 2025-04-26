import csv
import os
import sqlite3
from datetime import date, timedelta
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap, Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, select, Boolean, create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from cities import cities_in_california
import socket
from forms import LoginForm, SubmissionForm, ChangePasswordForm
import pandas as pd
import matplotlib.pyplot as plt

class Base(DeclarativeBase):
    pass
app = Flask(__name__)
with open('csrfkey.txt', 'r') as file:
    app.config['SECRET_KEY'] = file.readline().strip('\n')
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30) #Time the user out after 30 minutes
db = SQLAlchemy(model_class=Base)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

class Entry(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    city_of_residence: Mapped[str] = mapped_column(String, nullable=False)
    zipcode: Mapped[int] = mapped_column(Integer, nullable=False)
    referred_by: Mapped[str] = mapped_column(String, nullable=False)
    education: Mapped[str] = mapped_column(String, nullable=False)
    gender: Mapped[str] = mapped_column(String, nullable=False)
    ethnicity: Mapped[str] = mapped_column(String, nullable=False)
    race: Mapped[str] = mapped_column(String, nullable=False)
    housing: Mapped[str] = mapped_column(String, nullable=False)
    household_income: Mapped[int] = mapped_column(Integer, nullable=False)
    number_of_dependants: Mapped[int] = mapped_column(Integer, nullable=False)
    language: Mapped[str] = mapped_column(String, nullable=False)
    employment: Mapped[str] = mapped_column(String, nullable=False)
    health_coverage: Mapped[str] = mapped_column(String, nullable=False)
    hiv_status: Mapped[str] = mapped_column(String, nullable=False)
    lgbtq_status: Mapped[str] = mapped_column(String, nullable=False)
    veteran: Mapped[bool] = mapped_column(Boolean, nullable=False)

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))

def render_city_of_residence_plot():
    conn = None
    try:
        conn = sqlite3.connect('instance/users.db')
        query = "SELECT * FROM entry"
        df = pd.read_sql(query, conn)
        city_of_residence_df = df.groupby('city_of_residence').count().sort_values('age', ascending=False)
        ax1 = plt.gca()
        ax1.bar(city_of_residence_df.index, city_of_residence_df.age, color="blue")
        ax1.set_xlabel('city of residence')
        plt.xticks(fontsize=14, rotation=90)
        plt.tight_layout()
        plt.savefig('static/test.png')

    except sqlite3.Error as e:
        return f"Database Error: {e}", 500
    finally:
        if conn:
            conn.close()
def is_logged_in():
    if current_user.is_authenticated:
        return True
    return False

#Returns True if there are any registered users (Only the admin user should exist)
def admin_user_exists():
    users = db.session.execute(db.select(User)).scalar()
    if users:
        return True
    return False

# creates the admin user
def create_admin_user():
    db.session.add(User(name='admin', password=generate_password_hash('password', method="pbkdf2:sha256", salt_length=8)))
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

@login_manager.user_loader
def load_user(user_id):
    user_to_load = db.session.execute(select(User).where(User.id == user_id)).scalar()
    if user_to_load:
        return user_to_load
    else:
        return None
@app.route('/', methods=['GET', 'POST'])
def home():
    if not admin_user_exists():
        create_admin_user()

    form = LoginForm(stored_password=db.session.execute(db.select(User).where(User.name == 'admin')).scalar().password)
    if request.method == 'GET':
        return render_template("index.html", form=form, is_logged_in=is_logged_in())
    if not form.validate():
        return render_template('index.html', form=form, errors=form.errors, is_logged_in=is_logged_in())
    login_user(db.session.execute(db.select(User).where(User.name == 'admin')).scalar())
    if form.change_password.data:
        return redirect(url_for('change_password'))
    return redirect(url_for('form'))

@app.route('/form', methods=['GET', 'POST'])
@login_required
def form():
    form = SubmissionForm()
    if request.method == 'GET':
        return render_template('form_page.html', form=form, is_logged_in=is_logged_in(), cities_in_california=cities_in_california())
    if not form.validate():
        for error in form.errors:
            flash(error)
        return render_template('form_page.html', errors=form.errors, form=form, is_logged_in=is_logged_in(), cities_in_california=cities_in_california())
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
        return render_template('change_password.html', form=form, is_logged_in=is_logged_in())
    if not form.validate():
        return render_template('change_password.html', form=form, errors=form.errors, is_logged_in=is_logged_in())
    if form.password.data != form.confirm_password.data:
        flash('Passwords do not match')
        return render_template('change_password.html', form=form, errors=form.errors, is_logged_in=is_logged_in())
    user = db.session.execute(db.select(User).where(User.name == 'admin')).scalar()
    user.password = generate_password_hash(password=form.password.data, method='pbkdf2:sha256', salt_length=8)
    db.session.commit()
    flash('Your password has been changed')
    return redirect(url_for('home'))

@app.route('/statistics')
def statistics():
    render_city_of_residence_plot()
    return render_template('statistics.html')

@app.route('/reset', methods=['GET'])
def reset():
    user = db.session.execute(db.select(User).where(User.name == 'admin')).scalar()
    user.password = generate_password_hash(password='password', method='pbkdf2:sha256', salt_length=8)
    db.session.commit()
    flash("Your password has been reset")
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    form = LoginForm(stored_password=db.session.execute(db.select(User).where(User.name == 'admin')).scalar().password)
    if request.method == 'POST':
        if not form.validate():
            return redirect(url_for('login'))
        login_user(db.session.execute(db.select(User).where(User.name == 'admin')).scalar())
        return redirect(url_for('home'))
    else:
        return render_template('login.html', form=form, errors=form.errors, is_logged_in=is_logged_in())

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/test')
def test():
    conn = None
    try:
        conn = sqlite3.connect('instance/users.db')
        query = "SELECT * FROM entry"
        df = pd.read_sql(query, conn)
        print(df.age.mean())
    except sqlite3.Error as e:
        return f"Database Error: {e}", 500
    finally:
        if conn:
            conn.close()
    return redirect(url_for('home'))



def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if not database_exists():
    create_database()


if __name__ == "__main__":
    app.run(debug=True, port=5002, host=get_ip())
    #                              host='192.168.86.53'
