'''
This module contains the functions and classes to handle data access.
'''

import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.processing.constants import BASE_DIRECTORY

engine = create_engine(f'sqlite:///{BASE_DIRECTORY}/data/processed/db.sqlite', echo=False)
engine.connect()
Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session() # Session to import

