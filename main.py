from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'safjsafasfjks'
ckeditor = CKEditor(app)
Bootstrap(app)

class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login', render_kw={'class': 'btn custom-btn'})

@app.route('/')
def home():
    form = LoginForm()
    return render_template("index.html", form=form)

if __name__ == "__main__":
    app.run(debug=True, port=5002, host='172.16.249.198')