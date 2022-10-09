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


class User(UserMixin, db.Model):
    '''User Model'''
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)

    user_name = db.Column(db.String(100), unique=True, nullable=False)
    pw_hash = db.Column(db.String(200), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    phone = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)

    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy=True)
    events = db.relationship('Event', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

    def get_id(self):
        '''
        Override UserMixin get_id method to check user_id instead of id
        '''
        return str(self.user_id)

    def __repr__(self):
        return '<User {0}>'.format(self.email)


class Event(db.Model):
    '''Event Model'''
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum(EventStatus),
                       default=EventStatus.UNPUBLISHED,
                       nullable=False)

    image = db.Column(db.LargeBinary, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    venue = db.Column(db.String(100), nullable=False)

    time = db.Column(db.DateTime(timezone=False), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    ticket_price = db.Column(db.Numeric(scale=2), nullable=False)

    # Relationships
    comments = db.relationship('Comment', backref='event', lazy=True)
    bookings = db.relationship('Booking', backref='event', lazy=True)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    def __repr__(self):
        return '<Event {0}>'.format(self.title)


class Booking(db.Model):
    '''Booking Model'''
    __tablename__ = 'bookings'
    booking_id = db.Column(db.Integer, primary_key=True)

    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(scale=2), nullable=False)
    time = db.Column(db.DateTime(timezone=False), nullable=False)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)

    def __repr__(self):
        return '<Booking: {0}, Event: {1} User: {2}>'.format(
            self.booking_id, self.event_id, self.user_id)


class Comment(db.Model):
    '''Comment Model'''
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.String(1000), nullable=False)
    time = db.Column(db.DateTime(timezone=False), nullable=False)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)

    def __repr__(self):
        return '<Comment: {0}, Event: {1} User: {2}>'.format(
            self.comment_id, self.event_id, self.user_id)
