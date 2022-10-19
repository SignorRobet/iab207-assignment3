from flask import Blueprint, render_template
from flask_login import login_required


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
def concert():
    return render_template('concert.html', title='Concert')
