from dataclasses import dataclass
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from .models import Event, Booking, Comment
from .forms import BookingForm, CommentForm, CreateEventForm, LoginForm
from . import db
import os
from werkzeug.utils import secure_filename
from .functions import check_upload_file



bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    events = Event.query.all()    
    return render_template('index.html', title='Home', events=events)


@bp.route('/searchresults')
def searchresults():
    return render_template('searchresults.html', title='Search Results')


@bp.route('/myconcerts')
@login_required
def myconcerts():
    disp_bookings = Booking.query.all()
    disp_events = Event.query.all()
    return render_template('myconcerts.html', title='My Concerts')

@bp.route('/createevent', methods = ['GET', 'POST'])
# @login_required --- left for now while creating page so easy to view 
def createevent():
    form = CreateEventForm()
    if (form.validate_on_submit() == True):
        print("The form has been submitted")
        event = Event(id = form.eventID.data,
        title = form.eventname.data, 
        status = form.status.data, 
        image = check_upload_file(form.image.data, 'events'),
        description = form.info.data, 
        venue = form.venue.data, 
        time = form.dateTime.data, 
        capacity = form.tickets.data,
        ticket_price = form.price.data,
        user_id = 500)
  
        
        db.session.add(event)
        db.session.commit()
        # get all the db stuff connected
        # more db fields or less form options 
        return redirect(url_for('main.index'))
        
    return render_template('/eventCreation.html', form=form)

# def check_upload_file(form):
#   # Get the data for the file from the create event form  
#   fp=form.image.data
#   filename=fp.filename
#   #Construting a file directory path up until this point   
#   BASE_PATH=os.path.dirname(__file__)
#   upload_path=os.path.join(BASE_PATH,'/static/image/',secure_filename(filename))
#   db_upload_path='/static/image/' + secure_filename(filename)
#   # Saves as a local image 
#   fp.save(upload_path)
#   return db_upload_path

@bp.route('/concert/<id>')
def concert(id):
    concert = Event.query.filter_by(id=1).first()
    comment_form = CommentForm()
    booking_form = BookingForm()
    return render_template(
        'concert.html',
        title='Concert',
        concert=concert,
        comment_form=comment_form,
        booking_form=booking_form
    )
