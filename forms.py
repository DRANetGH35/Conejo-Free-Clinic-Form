from wtforms.fields import PasswordField, SubmitField, StringField, IntegerField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash

def ensure_positive_number(form, field):
    print(field.data)
    if field.data < 0:
        raise ValidationError('Enter a positive number')

class ChangePasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Submit', render_kw={'class': 'btn custom-btn'})

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    change_password = BooleanField('Change Password')
    submit = SubmitField('Login', render_kw={'class': 'btn custom-btn'})

    def __init__(self, stored_password=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stored_password = stored_password

    def validate_password(self, field):
        if not check_password_hash(pwhash=self.stored_password, password=field.data):
            raise ValidationError('Passwords do not match')




class SubmissionForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired(), ensure_positive_number])
    city_of_residence = StringField('City of Residence', validators=[DataRequired()])
    zipcode = IntegerField('Zipcode', validators=[DataRequired(), ensure_positive_number])
    referred_by = SelectField('Referred by', choices=[('Friend', 'Friend'),
                                                          ('Family', 'Family'),
                                                          ('Other', 'Other')])

    education = SelectField('Education', choices=[('Grade School', 'Grade School'),
                                                       ('Some High School', 'Some High School'),
                                                       ('GED', 'GED'),
                                                       ('Some College', 'Some College'),
                                                       ('College Degree', 'College Degree'),
                                                       ('None', 'None')])

    gender = SelectField("Gender", choices=[('Male', 'Male'),
                                                 ('Female', 'Female'),
                                                 ('Other', 'Other'),
                                                 ('Decline to answer', 'Decline to answer')])

    ethnicity = SelectField('Ethnicity', choices=[('Hispanic/Latino', 'Hispanic/Latino'),
                                                       ('White/Caucasian', 'White/Caucasian'),
                                                       ('Unknown', 'Unknown')])

    race = SelectField('Race', choices=[('Caucasian', 'Caucasian'),
                                             ('Black', 'Black'),
                                             ('Asian', 'Asian'),
                                             ('Native American', 'Native American'),
                                             ('Pacific Islander', 'Pacific Islander'),
                                             ('Multi-racial', 'Multi-racial'),
                                             ('Other', 'Other')])

    housing = SelectField('Housing', choices=[('Apartment', 'Apartment'),
                                                   ('Public Shelter', 'Public Shelter'),
                                                   ('Near Homeless', 'Near Homeless'),
                                                   ('Private Home', 'Private Home'),
                                                   ('Car/Street Trailer','Car/Street Trailer'),
                                                   ('Un-Housed', 'Un-Housed')])
    household_income = IntegerField('Household Income (Monthly)', validators=[DataRequired(), ensure_positive_number])
    number_of_dependants = IntegerField('Number of Dependents in Household', validators=[DataRequired(), ensure_positive_number])
    language = SelectField('Language', choices=[('English', 'English'),
                                                        ('Spanish', 'Spanish')])
    employment = SelectField('Employment', choices=[('Community', 'Community'),
                                                         ('Unemployed', 'Unemployed'),
                                                         ('Disabled', 'Disabled'),
                                                         ('Full-Time', 'Full-Time'),
                                                         ('Part-Time', 'Part-Time'),
                                                         ('Seasonal', 'Seasonal'),
                                                         ('Student', 'Student')])
    health_coverage = SelectField("Health Coverage", choices=[('Medicare without part B', 'Medicare without part B'),
                                                                    ('Private Insurance', 'Private Insurance'),
                                                                    ('Covered California', 'Covered California'),
                                                                    ('None', 'None')])
    hiv_status = SelectField('HIV Status', choices=[('N/A', 'N/A'),
                                                        ('HIV+', 'HIV+'),
                                                        ('HIV+, AIDS Status unknown', 'HIV+, AIDS Status unknown'),
                                                        ('CDC-Defined AIDS', 'CDC-Defined AIDS')])
    lgbtq_status = SelectField('Member of LGBTQ+', choices=[('Yes', 'Yes'),
                                                                ('No', 'No'),
                                                                ('Decline to answer', 'Decline to answer')])
    veteran = BooleanField('Veteran')

    submit = SubmitField('Submit', render_kw={'class': 'btn custom-btn'})