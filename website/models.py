# Project:    IAB207 Assignment 3 - Group 12
# Document:   models.py
# Author:     Simon Di Florio
# Date:       05/10/2022
#
# This Python script defines each of the database classes.

import enum
from . import db


class EventStatus(enum.Enum):
    '''Enum for the status of an event'''
    OPEN = 'Open'
    UNPUBLISHED = 'Unpublished'
    SOLD_OUT = 'Sold-out'
    CANCELLED = 'Cancelled'


class User(db.Model):
    '''User Model'''
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)

    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy=True)
    events = db.relationship('Event', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

    def __init__(self, email, password, first_name, last_name, phone, dob):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.dob = dob

    def __repr__(self):
        return '<User {0}>'.format(self.email)


class Event(db.Model):
    '''Event Model'''
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(EventStatus),
                       default=EventStatus.UNPUBLISHED,
                       nullable=False)
    title = db.Column(db.String(100), nullable=False)

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

    def __init__(self, status, title,
                 image, description, venue,
                 time, capacity, ticket_price, user_id):
        self.status = status
        self.title = title

        self.image = image
        self.description = description
        self.venue = venue

        self.time = time
        self.capacity = capacity
        self.ticket_price = ticket_price

        self.user_id = user_id

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

    def __init__(self, quantity, price, time, user_id, event_id):
        self.quantity = quantity
        self.price = price
        self.time = time

        self.user_id = user_id
        self.event_id = event_id

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

    def __init__(self, text, time, user_id, event_id):
        self.text = text
        self.time = time

        self.user_id = user_id
        self.event_id = event_id

    def __repr__(self):
        return '<Comment: {0}, Event: {1} User: {2}>'.format(
            self.comment_id, self.event_id, self.user_id)
