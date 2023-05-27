"""
This file contains the models for the shortener_app's database.

Author: Alex Wendland
"""

# These are types for the data in the database.
from sqlalchemy import Boolean, Column, Integer, String

# This is the database class.
from .database import session_base


# This is the model for the urls being stored in the database.
class URL(session_base):
    """
    This is the model for the urls being stored in the database.
    """

    # By default table names are plurals of the class name.
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)
