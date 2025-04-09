from wtforms.fields import PasswordField, SubmitField, StringField, IntegerField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login', render_kw={'class': 'btn custom-btn'})

class SubmissionForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired()])
    city_of_residence = StringField('City of Residence', validators=[DataRequired()])
    zipcode = IntegerField('Zipcode', validators=[DataRequired()])
    referred_by = SelectField('Referred by', validators=[DataRequired()], choices=[('Friend', 'Friend'),
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
    household_income = IntegerField('Household Income (Monthly)', validators=[DataRequired()])
    number_of_dependants = IntegerField('Number of Dependents in Household', validators=[DataRequired()])
    language = SelectField('Language', validators=[DataRequired()], choices=[('English', 'English'), ('Spanish', 'Spanish')])
    employment = SelectField('Employment', validators=[DataRequired()], choices=[('Community', 'Community'),
                                                                                 ('Unemplyoed', 'Unemplyoed'),
                                                                                 ('Disabled', 'Disabled'),
                                                                                 ('Full-Time', 'Full-Time'),
                                                                                 ('Part-Time', 'Part-Time'),
                                                                                 ('Seasonal', 'Seasonal'),
                                                                                 ('Student', 'Student')])
    health_coverage = SelectField("Health Coverage", validators=[DataRequired()], choices=[('Medicare without part B', 'Medicare without part B'),
                                                                                                ('Private Insurance', 'Private Insurance'),
                                                                                                ('Covered California', 'Covered California'),
                                                                                                ('None', 'None')])
    hiv_status = SelectField('HIV Status', validators=[DataRequired()], choices=[('HIV+', 'HIV+'),
                                                                                        ('HIV+, AIDS Status unknown', 'HIV+, AIDS Status unknown'),
                                                                                        ('CDC-Defined AIDS', 'CDC-Defined AIDS')])
    lgbtq_status = SelectField('Member of LGBTQ+', validators=[DataRequired()], choices=[('Yes', 'Yes'),
                                                                                            ('No', 'No'),
                                                                                            ('Decline to answer', 'Decline to answer')])
    veteran = BooleanField('Veteran', validators=[DataRequired()])

    submit = SubmitField('Submit', render_kw={'class': 'btn custom-btn'})