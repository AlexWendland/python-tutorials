"""
This module contains all helper functions for key generation.

Author: Alex Wendland
"""

# Secrets is the recommended way to generate random keys.
import secrets

# This is the library that contains all the characters.
import string

from sqlalchemy.orm import Session

from . import database_queries


def create_random_generic_key(length: int = 5) -> str:
    """
    This function creates a random key of a given length.

    Args:
        length (int, optional): The length of the key. Defaults to 5.

    Returns:
        str: The key.
    """
    if length <= 0:
        raise ValueError("Key length must be greater than 0.")

    return "".join(
        secrets.choice(string.ascii_letters + string.digits) for _ in range(length)
    )


def create_unique_random_key(database: Session, length: int = 5) -> str:
    """
    This function creates a unique random key for the database.

    Args:
        database (Session): The database session.
        length (int, optional): The length of the key. Defaults to 5.

    Returns:
        str: The key.
    """
    key = create_random_generic_key(length)

    while database_queries.get_database_url_by_key(database, key):
        key = create_random_generic_key(length)

    return key
