/* 
 Project:    IAB207 Assignment 3 - Group 12
 Document:   init.sql
 Author:     Simon Di Florio
 Date:       05/10/2022
 
 THIS FILE IS UNUSED
 
 This SQL file generates the PostgreSQL database for the application
 and clears the contents of every table.
 */
;
/* Create Database and connect to it */
/* Users Table */
CREATE TABLE IF NOT EXISTS Users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    dob DATE NOT NULL
);
/* Events Table and status enum */
CREATE TYPE event_status AS ENUM (
    'Open',
    'Unpublished',
    'Sold-out',
    'Cancelled'
);
CREATE TABLE IF NOT EXISTS Events (
    event_id SERIAL PRIMARY KEY,
    owner_id INTEGER references Users(user_id),
    title VARCHAR(100) UNIQUE NOT NULL,
    status event_status NOT NULL,
    event_timestamp TIMESTAMPTZ NOT NULL,
    image BYTEA,
    ticket_price MONEY NOT NULL CHECK (ticket_price >= cast(0 AS money)),
    ticket_quantity INTEGER NOT NULL CHECK (ticket_quantity > 0)
);
/* Bookings Table */
CREATE TABLE IF NOT EXISTS Bookings (
    booking_id SERIAL PRIMARY KEY,
    event_id INTEGER references Events(event_id),
    user_id INTEGER references Users(user_id),
    ticket_quantity INTEGER NOT NULL CHECK (ticket_quantity > 0),
    total_price MONEY NOT NULL CHECK (total_price >= cast(0 AS money)),
    booking_timestamp TIMESTAMPTZ NOT NULL
);
/* Comments Table */
CREATE TABLE IF NOT EXISTS Comments (
    comment_id SERIAL PRIMARY KEY,
    event_id INTEGER references Events(event_id),
    user_id INTEGER references Users(user_id),
    comment TEXT NOT NULL,
    comment_timestamp TIMESTAMPTZ NOT NULL
);
/* Clear table contents, then populate with default data */
TRUNCATE TABLE Users,
Events,
Bookings,
Comments RESTART IDENTITY;