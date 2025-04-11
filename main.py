import os
from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, select
from werkzeug.security import generate_password_hash, check_password_hash
from cities import cities_in_california
import socket
from forms import LoginForm, SubmissionForm


class Base(DeclarativeBase):
    pass
app = Flask(__name__)
with open('csrfkey.txt', 'r') as file:
    app.config['SECRET_KEY'] = file.readline().strip('\n')
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
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


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))

#Returns True if there are any registered users (Only the admin user should exist)
def admin_user_exists():
    users = db.session.execute(db.select(User)).scalar()
    if users:
        return True
    return False
# creates the admin user
def create_admin_user():
    db.session.add(User(name='admin', password='password'))
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

    form = LoginForm()
    if request.method == 'GET':
        return render_template("index.html", form=form)
    if request.method == 'POST':
        if form.validate():
            return redirect(url_for('form'))
@app.route('/form', methods=['GET', 'POST'])
def form():
    form = SubmissionForm()
    if request.method == 'GET':
        return render_template('form_page.html', form=form, cities_in_california=cities_in_california())
    if request.method == 'POST':
        if form.validate_on_submit():
            return render_template('success.html')
@app.route('/test')
def test():
    print(admin_user_exists())
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
