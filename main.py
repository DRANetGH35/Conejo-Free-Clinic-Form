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
from wtforms.fields import PasswordField, SubmitField, StringField, IntegerField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'safjsafasfjks'
ckeditor = CKEditor(app)
Bootstrap(app)

class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login', render_kw={'class': 'btn custom-btn'})

class SubmissionForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired()])
    cityofresidence = StringField('City of Residence', validators=[DataRequired()])
    zipcode = IntegerField('Zipcode', validators=[DataRequired()])
    referredby = SelectField('Referred by', validators=[DataRequired()], choices=[('Friend', 'Friend'),
                                                                                      ('Family', 'Family'),
                                                                                      ('Other', 'Other')])

    education = SelectField('Education', validators=[DataRequired()], choices=[('Grade School', 'Grade School'),
                                                                                   ('Some High School', 'Some High School'),
                                                                                   ('GED', 'GED'),
                                                                                   ('Some College', 'Some College'),
                                                                                   ('College Degree', 'College Degree'),
                                                                                   ('None', 'None')])

    gender = SelectField("Gender", validators=[DataRequired()], choices=[('Male', 'Male'),
                                                                             ('Female', 'Female'),
                                                                             ('Other', 'Other'),
                                                                             ('Decline to answer', 'Decline to answer')])

    ethnicity = SelectField('Ethnicity', validators=[DataRequired()], choices=[('Hispanic/Latino', 'Hispanic/Latino'),
                                                                                   ('White/Caucasian', 'White/Caucasian'),
                                                                                   ('Unknown', 'Unknown')])

    race = SelectField('Race', validators=[DataRequired()], choices=[('Caucasian', 'Caucasian'),
                                                                             ('Black', 'Black'),
                                                                             ('Asian', 'Asian'),
                                                                             ('Native American', 'Native American'),
                                                                             ('Pacific Islander', 'Pacific Islander'),
                                                                             ('Multi-racial', 'Multi-racial'),
                                                                             ('Other', 'Other')])

    housing = SelectField('Housing', validators=[DataRequired()], choices=[('Apartment', 'Apartment'),
                                                                               ('Public Shelter', 'Public Shelter'),
                                                                               ('Near Homeless', 'Near Homeless'),
                                                                               ('Private Home', 'Private Home'),
                                                                               ('Car/Street Trailer','Car/Street Trailer'),
                                                                               ('Homeless', 'Homeless')])
    number_of_dependants = IntegerField('Number of Dependents in Household', validators=[DataRequired()])
    language = SelectField('Language', validators=[DataRequired()], choices=[('English', 'English'), ('Spanish', 'Spanish')])

    veteran = BooleanField('Veteran', validators=[DataRequired()])

@app.route('/')
def home():
    form = LoginForm()
    return render_template("index.html", form=form)

@app.route('/form_page')
def form_page():
    form = SubmissionForm()
    return render_template('form_page.html', form=form)

if __name__ == "__main__":
    app.run(debug=True, port=5002, host='172.16.249.198')