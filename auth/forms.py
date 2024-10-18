from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
class LoginForm(FlaskForm):
    login_identifier = StringField('Email or Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[Optional()])
    middle_name = StringField('Middle Name', validators=[Optional()])
    last_name = StringField('Last Name', validators=[Optional()])
    
    department = SelectField('Department', choices=[
        ('HR', 'Human Resources'),
        ('IT', 'Information Technology'),
        ('Finance', 'Finance'),
        ('Marketing', 'Marketing'),
        ('Operations', 'Operations'),
        ('Legal', 'Legal')
    ], validators=[DataRequired()])
    
    phone_number = StringField('Phone Number', validators=[Optional()])
    address = StringField('Address', validators=[Optional()])
    
    submit = SubmitField('Update Profile')