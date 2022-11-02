from dataclasses import dataclass
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime

from .models import Event, Booking, Comment
from .forms import BookingForm, CommentForm, CreateEventForm, LoginForm
from . import db
from .functions import check_upload_file


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html', title='Home')


@bp.route('/searchresults')
def searchresults():
    return render_template('searchresults.html', title='Search Results')


@bp.route('/myconcerts')
@login_required
def myconcerts():
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

    return render_template('/eventCreation.html', form=form, title="Create Concert")


@bp.route('/concert/<id>', methods=['GET', 'POST'])
def concert(id):
    concert = Event.query.filter_by(id=id).first()
    comment_form = CommentForm()
    booking_form = BookingForm()

    if (booking_form.booking_submit.data and booking_form.validate()):
        print("In Booking form submission")
        booking = Booking(user_id=current_user.id,
                          event_id=concert.id,
                          quantity=booking_form.quantity.data,
                          price=(concert.ticket_price * booking_form.quantity.data),
                          time=datetime.now())

        db.session.add(booking)
        db.session.commit()
        return redirect(url_for('main.concert', id=id))

    if (comment_form.comment_submit.data and comment_form.validate()):
        print("In Comment form submission")
        comment = Comment(user_id=current_user.id,
                          event_id=concert.id,
                          text=comment_form.text.data,
                          time=datetime.now()
                          )

        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('main.concert', id=id))

    return render_template(
        'concert.html',
        title='Concert',
        concert=concert,
        comment_form=comment_form,
        booking_form=booking_form
    )
