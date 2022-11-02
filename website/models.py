# Project:    IAB207 Assignment 3 - Group 12
# Document:   models.py
# Author:     Simon Di Florio
# Date:       05/10/2022
#
# This Python script defines each of the database classes.

# README for constructor behaviour
# https://stackoverflow.com/questions/20460339/flask-sqlalchemy-constructor

import enum
from . import db
from flask_login import UserMixin


class EventStatus(enum.Enum):
    '''Enum for the status of an event'''
    OPEN = 'Open'
    UNPUBLISHED = 'Unpublished'
    SOLD_OUT = 'Sold-out'
    CANCELLED = 'Cancelled'

class Genre(enum.Enum):
    ROCK = 'Rock'
    ALTERNATIVE = 'Alternative'
    BLUES = 'Blues'
    POP = 'Pop'
    COUNTRY = 'Country'
    CLASSICAL = 'Classical'
    EDM = 'EDM'
    JAZZ = 'Jazz'




class User(UserMixin, db.Model):
    '''User Model'''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    user_name = db.Column(db.String(40), unique=True, nullable=False)
    pw_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    image = db.Column(db.String(200), nullable=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    phone = db.Column(db.String(50), nullable=True)
    dob = db.Column(db.Date, nullable=True)

    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy=True)
    events = db.relationship('Event', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

    def __repr__(self):
        return '<User {0}, username: {1}>'.format(self.id, self.user_name)


class Event(db.Model):
    '''Event Model'''
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum(EventStatus),
                       default=EventStatus.UNPUBLISHED,
                       nullable=False)
    genre = db.Column(db.Enum(Genre),
                        default=Genre.ROCK,
                        nullable=False)

    image = db.Column(db.String(200), nullable=True)
    description = db.Column(db.String(1000), nullable=False)
    venue = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)

    date = db.Column(db.Date, nullable=True)
    tome = db.Column(db.Time, nullable=True)

    # time = db.Column(db.DateTime(timezone=False), nullable=False)
    
    capacity = db.Column(db.Integer, nullable=False)
    ticket_price = db.Column(db.Numeric(scale=2), nullable=False)

    # Relationships
    comments = db.relationship('Comment', backref='event', lazy=True)
    bookings = db.relationship('Booking', backref='event', lazy=True)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return '<Event {0}, Title: {1}>'.format(self.id, self.title)


class Booking(db.Model):
    '''Booking Model'''
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)

    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(scale=2), nullable=False)
    time = db.Column(db.DateTime(timezone=False), nullable=False)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    def __repr__(self):
        return '<Booking: {0}, Event: {1}, User: {2}>'.format(
            self.id, self.event_id, self.user_id)


class Comment(db.Model):
    '''Comment Model'''
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.String(1000), nullable=False)
    time = db.Column(db.DateTime(timezone=False), nullable=False)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    def __repr__(self):
        return '<Comment: {0}, Event: {1} User: {2}>'.format(
            self.id, self.event_id, self.user_id)
