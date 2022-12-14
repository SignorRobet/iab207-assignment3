
from flask_wtf import FlaskForm
from wtforms.fields import (
    TextAreaField, SubmitField, StringField, PasswordField,
    DateField, SelectField, DateTimeField, RadioField,
    IntegerField, DecimalField, TimeField
)
from wtforms.validators import (
    InputRequired, Length, Email, EqualTo, Regexp, Optional, NumberRange)
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.widgets import TextArea

ALLOWED_IMAGE = {'PNG', 'JPG', 'png', 'jpg'}


# creates the login information
class LoginForm(FlaskForm):
    user_name = StringField("Username", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    '''
    This is the registration form
    '''
    user_name = StringField(
        "User Name",
        validators=[InputRequired(),
                    # TODO Rexexp validator not working
                    Regexp(
                        '[A-Za-z][A-Za-z0-9\-_]*[A-Za-z0-9]',
                        message=('User name can only contain letters, numbers, hypens and underscores.\n' +
                                 'Must start with a letter and end with a letter or number.')),
                    Length(
                        min=3, max=20, message='User name must be between 3 and 20 characters long')])

    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField(
        "Password",
        validators=[InputRequired(),
                    Length(min=4, message="Password must be at least 4 characters long"),
                    EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    image = FileField('Profile Picture', validators=[
        FileAllowed(ALLOWED_IMAGE, message='Only supports png, jpg, JPG, PNG')])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    phone = StringField("Phone", validators=[])
    dob = DateField("Date of Birth", validators=[Optional()])

    # submit button
    submit = SubmitField("Register")


class BookingForm(FlaskForm):
    '''
    WTForm for booking an event.

    Auto-populated fields:
    - user_id
    - event_id
    - booking_date
    - booking_time
    - price
    '''
    quantity = IntegerField("Ticket Quantity", validators=[
        InputRequired(),
        NumberRange(min=1, message="Ticket Quantity must be greater than 0")
    ])
    booking_submit = SubmitField("Book Tickets")


class CommentForm(FlaskForm):
    '''
    WTForm for commenting on an event.

    Auto-populated fields:
    - user_id
    - event_id
    - comment datetime
    '''
    text = TextAreaField("Write a comment...", validators=[InputRequired()])
    comment_submit = SubmitField("Submit")


class CreateEventForm(FlaskForm):
    eventname = StringField('Event Name', validators=[InputRequired()])
    genre = SelectField('Genre', choices=['ROCK', 'ALTERNATIVE', 'BLUES', 'POP', 'COUNTRY', 'CLASSICAL', 'EDM', 'JAZZ'])
    info = TextAreaField('Event Information', widget=TextArea(), validators=[Length(min=10), InputRequired()])
    artist = StringField('Artist', validators=[InputRequired()])

    date = DateField("Date of Event", validators=[Optional()])
    time = TimeField("Time of Event", validators=[Optional()])

    status = RadioField('Event Status',
                        choices=['OPEN', 'UNPUBLISHED', 'SOLD_OUT', 'CANCELLED'], default='OPEN')
    tickets = IntegerField('Available Tickets', validators=[InputRequired(),
                                                            NumberRange(min=1, message="Ticket Quantity must be greater than 0")])
    price = DecimalField('Price per Ticket', validators=[InputRequired(), NumberRange(min=0,
                                                         message="Ticket Price must be equal or greater than 0")],
                         places=2)

    submit = SubmitField("Create")
    image = FileField("Upload Event Image", validators=[
        FileAllowed(ALLOWED_IMAGE, message='Only supports png, jpg, JPG, PNG')])
    venue = StringField("Venue", validators=[InputRequired()])


class EditEventForm(FlaskForm):
    eventname = StringField('Event Name', validators=[InputRequired()])
    genre = SelectField('Genre', choices=['ROCK', 'ALTERNATIVE', 'BLUES', 'POP', 'COUNTRY', 'CLASSICAL', 'EDM', 'JAZZ'])
    info = TextAreaField('Event Information', widget=TextArea(), validators=[Length(min=10), InputRequired()])
    artist = StringField('Artist', validators=[InputRequired()])

    date = DateField("Date of Event", validators=[Optional()])
    time = TimeField("Time of Event", validators=[Optional()])

    status = RadioField('Event Status', choices=['OPEN', 'UNPUBLISHED', 'SOLD_OUT', 'CANCELLED'], default='OPEN')
    tickets = IntegerField('Available Tickets', validators=[InputRequired(
    ), NumberRange(min=1, message="Ticket Quantity must be greater than 0")])
    price = DecimalField('Price per Ticket', validators=[InputRequired(),
                                                         NumberRange(min=0,
                                                         message="Ticket Price must be equal or greater than 0")],
                         places=2)

    submit = SubmitField("Update Concert")
    image = FileField("Upload Event Image", validators=[
        FileAllowed(ALLOWED_IMAGE, message='Only supports png, jpg, JPG, PNG')])
    venue = StringField("Venue", validators=[InputRequired()])
