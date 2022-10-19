from flask import Blueprint, render_template
from flask_login import login_required
from .models import Event, Booking, Comment
from .forms import BookingForm, CommentForm


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
