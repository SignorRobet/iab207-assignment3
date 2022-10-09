# import flask - from the package import class
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# import os

db = SQLAlchemy()


def create_app():
    '''
    Create Flask Web Application
    '''

    app = Flask(__name__)  # this is the name of the module/package that is calling this app
    app.debug = True
    app.secret_key = 'utroutoru'

    # set the app configuration data
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    # app.config['SQLALCHEMY_DATABASE_URI']=os.environ['DATABASE_URL']

    # initialise db with flask app and create tables
    db.init_app(app)
    from .models import User, Event, Booking, Comment
    db.create_all(app=app)

    # db.session.add(User)

    bootstrap = Bootstrap5(app)

    # initialise the login manager
    login_manager = LoginManager()

    # set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # importing views module here to avoid circular references
    # a commonly used practice.
    from . import views
    app.register_blueprint(views.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    return app
