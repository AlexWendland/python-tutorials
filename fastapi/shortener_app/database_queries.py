"""
This runs simple database queries.

Author: Alex Wendland
"""

from sqlalchemy.orm import Session

from . import models


def get_database_url_by_key(database: Session, url_key: str) -> models.URL:
    """
    Gets a URL from the database by its key.

    Args:
        database (Session): The database session.
        url_key (str): The key of the URL.

    Returns:
        models.URL: The URL model.
    """
    return database.query(models.URL).filter(models.URL.key == url_key).first()


def get_active_database_url_by_key(database: Session, url_key: str) -> models.URL:
    """
    Gets an active URL from the database by its key.

    Args:
        database (Session): The database session.
        url_key (str): The key of the URL.

    Returns:
        models.URL: The URL model.
    """
    return (
        database.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )


def get_active_database_url_by_secret_key(
    database: Session, secret_key: str
) -> models.URL:
    """
    Gets an active URL from the database by its secret key.

    Args:
        database (Session): The database session.
        secret_key (str): The secret key of the URL.

    Returns:
        models.URL: The URL model.
    """
    return (
        database.query(models.URL)
        .filter(models.URL.secret_key == secret_key, models.URL.is_active)
        .first()
    )
