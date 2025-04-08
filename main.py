from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from werkzeug.security import generate_password_hash, check_password_hash

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


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))

@app.route('/', methods=['GET', 'POST'])
def home():
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
        return render_template('form_page.html', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            return render_template('success.html')
if __name__ == "__main__":
    app.run(debug=True, port=5002)