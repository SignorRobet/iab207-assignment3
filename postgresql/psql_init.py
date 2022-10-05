# Project:    IAB207 Assignment 3 - Group 12
# Document:   psql_init.py
# Author:     Simon Di Florio
# Date:       05/10/2022
#
# This Python script generates some default data for the PostgreSQL database.
# Note that the database needs to be created first

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from local_settings import postgresql as settings


def get_engine(user, passwd, host, port, db):
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, pool_size=50, echo=False)
    return engine


if __name__ == "__main__":
    engine = get_engine(settings['pguser'],
                        settings['pgpasswd'],
                        settings['pghost'],
                        settings['pgport'],
                        settings['pgdb'])
