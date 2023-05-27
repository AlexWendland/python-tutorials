"""
This module contains the configuration of the application.

Author: Alex Wendland
"""
# This decorator caches the data.
from functools import lru_cache

# This is a library that allows us to use environment variables.
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    This class contains the settings for the application.
    """

    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./shortener.db"

    class Config:
        """
        This will load the values from a .env file if it exists.
        """

        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """
    This function gets the settings for the application.

    Returns:
        Settings: The settings for the application.
    """
    settings = Settings()
    print(f"Environment: {settings.env_name}")
    return settings
