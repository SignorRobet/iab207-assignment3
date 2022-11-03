from flask import (
    Blueprint, render_template, request, redirect, url_for, flash
)
from flask_login import login_required, current_user

from datetime import datetime

from .models import Event, Booking, Comment
from .forms import BookingForm, CommentForm, CreateEventForm
from . import db
from .functions import check_upload_file


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', title='Home', events=events)


@bp.route('/searchresults')
def searchresults():
    return render_template('searchresults.html', title='Search Results')


@bp.route('/search')
def search():
    if request.args['search']:
        print(request.args['search'])
        dest = "%" + request.args['search'] + '%'
        events = Event.query.filter(Event.title.like(dest)).all()
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))


@bp.route('/genre')
def genre():
    if request.args['genre']:
        print(request.args['genre'])
        dest = request.args['genre']
        if (dest == 'all'):
            events = Event.query.all()
        else:
            events = Event.query.filter(Event.genre == dest).all()
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))


@bp.route('/myconcerts')
@login_required
def myconcerts():
    disp_bookings = Booking.query.all()
    disp_events = Event.query.all()
    return render_template('myconcerts.html', title='My Concerts', disp_events=disp_events, disp_bookings=disp_bookings)


@bp.route('/createevent', methods=['GET', 'POST'])
# @login_required --- left for now while creating page so easy to view
def createevent():
    form = CreateEventForm()

    if (form.validate_on_submit() == True):
        print("Event form has been submitted")
        event = Event(
            title=form.eventname.data,
            artist=form.artist.data,
            genre=form.genre.data,
            status=form.status.data,
            image=check_upload_file(form.image.data, 'events'),
            description=form.info.data,
            venue=form.venue.data,
            date=form.date.data,
            time=form.time.data,
            capacity=form.tickets.data,
            ticket_price=form.price.data,
            user_id=current_user.id)

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
    message = None

    if (booking_form.booking_submit.data and booking_form.validate()):
        print("In Booking form submission")
        booking = Booking(user_id=current_user.id,
                          event_id=concert.id,
                          quantity=booking_form.quantity.data,
                          price=(concert.ticket_price * booking_form.quantity.data),
                          time=datetime.now())

        # check if enough tickets are available, if not, don't add to db
        tickets_left = concert.capacity - concert.tickets_booked
        if (booking.quantity > tickets_left):
            message = """Booking Failed: Not enough tickets available.
            Only {0} tickets remaining""".format(tickets_left)
        else:
            # add booking to db and update concert tickets booked / status if relevant
            concert.tickets_booked = concert.tickets_booked + booking.quantity  # += is apparently bad practice
            if (concert.tickets_booked >= concert.capacity):
                concert.status = "SOLD_OUT"
            db.session.add(booking)
            db.session.commit()
            message = "Successfully booked tickets"

        flash(message)
        return redirect(url_for('main.concert', id=id))

    if (comment_form.comment_submit.data and comment_form.validate()):
        print("In Comment form submission")

        comment = Comment(user_id=current_user.id,
                          event_id=concert.id,
                          text=comment_form.text.data,
                          time=datetime.now())

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
