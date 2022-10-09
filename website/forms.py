
from flask_wtf import FlaskForm
from wtforms.fields import (
    TextAreaField, SubmitField, StringField, PasswordField,
    DateField
)
from wtforms.validators import InputRequired, Length, Email, EqualTo


# creates the login information
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    '''
    This is the registration form
    '''
    user_name = StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                                                     EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    phone = StringField("Phone", validators=[InputRequired()])
    dob = DateField("Date of Birth", validators=[InputRequired()])

    # submit button
    submit = SubmitField("Register")
