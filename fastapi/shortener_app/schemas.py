"""
This module contains the schemas for the API.

Author: Alex Wendland
"""

from pydantic import BaseModel


class URL(BaseModel):
    """
    This is the base schema for the URL.
    """

    target_url: str


class EnrichedURL(URL):
    """
    This contains the URL with metadata.
    """

    is_active: bool
    clicks: int

    class Config:
        orm_mode = True


class URLInfo(EnrichedURL):
    """
    This houses the processed URL information.
    """

    url: str
    admin_url: str
