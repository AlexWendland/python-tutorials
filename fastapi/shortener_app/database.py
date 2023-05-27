"""
This module contains the will make and run the database.

Author: Alex Wendland
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import get_settings

engine = create_engine(get_settings().db_url, connect_args={"check_same_thread": False})
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session_base = declarative_base()
