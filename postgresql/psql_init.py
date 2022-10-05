# Project:    IAB207 Assignment 3 - Group 12
# Document:   psql_init.py
# Author:     Simon Di Florio
# Date:       05/10/2022
#
# THIS FILE IS UNUSED
#
# This Python script generates some default data for the PostgreSQL database.
# Note that the database needs to be created first

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


def get_engine(user, passwd, host, port, db):
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, pool_size=50, echo=False)
    return engine


if __name__ == "__main__":
    engine = get_engine('postgres',
                        'postgres',
                        'localhost',
                        '5432',
                        'iab207-group12')

    Session = sessionmaker(bind=engine)
    s = Session()

    s.close()
