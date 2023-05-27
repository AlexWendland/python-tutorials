"""
This is the main file for running the fast API.

Author: Alex Wendland
"""

# This library is used to validated URLS
import validators

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse


from sqlalchemy.orm import Session
from starlette.datastructures import URL

from . import crud, database_queries, models, schemas

# This imports connections to our database.
from .database import local_session, engine
from .config import get_settings

app = FastAPI()
models.session_base.metadata.create_all(bind=engine)


def get_database() -> Session:
    """
    This function is used to get the database session.

    Yields:
        Session: The database session.
    """
    database = local_session()
    try:
        yield database
    finally:
        database.close()


def get_admin_info(database_url: models.URL) -> schemas.URLInfo:
    """
    The function gets the admin info for a URL, enriching it with the data from
    settings.

    Args:
        database_url (models.URL): The URL information from the database.

    Returns:
        schemas.URLInfo: The URL information for the API.
    """
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "administration info", secret_key=database_url.secret_key
    )

    return schemas.URLInfo(
        target_url=database_url.target_url,
        is_active=database_url.is_active,
        clicks=database_url.clicks,
        url=str(base_url.replace(path=database_url.key)),
        admin_url=str(base_url.replace(path=admin_endpoint)),
    )


def raise_bad_request(message: str):
    """
    This function raises a bad request error.

    Args:
        message (str): The desired message.

    Raises:
        HTTPException: The bad request error.
    """
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request: Request):
    """
    This function raises a not found error.

    Args:
        request (Request): The request that was made.

    Raises:
        HTTPException: The not found error.
    """
    message = f"URL not found: {request.url}"
    raise HTTPException(status_code=404, detail=message)


@app.get("/")
def read_root() -> str:
    """
    The main route for the API.

    Returns:
        str: The main page, not very useful.
    """
    return (
        "The website shortens URLs. OpenAPI docs can be found at: "
        f"{get_settings().base_url}/docs"
    )


@app.post("/url", response_model=schemas.URLInfo)
def process_new_url(
    url: schemas.URL, database: Session = Depends(get_database)
) -> schemas.URLInfo:
    """
    The function creates a URL entry in the database and shortens it.

    Args:
        url (schemas.URL): The URL to be shortened and added to the database.
        database (Session, optional): The database session. Defaults to
            Depends(get_database).

    Returns:
        schema.URLInfo: The information about the shortened URL.
    """
    if not validators.url(url.target_url):
        raise_bad_request("Invalid URL")

    database_url = crud.create_database_url(database=database, url=url)

    return get_admin_info(database_url)


@app.get("/{url_key}")
def forward_to_target_url(
    url_key: str, request: Request, database: Session = Depends(get_database)
) -> RedirectResponse:
    """
    Redirect for shortened URLs.

    Args:
        url_key (str): The shortened URL key.
        request (Request): The request that was made.
        database (Session, optional): The database session. Defaults to
            Depends(get_database).

    Returns:
        RedirectResponse: The redirect to the target URL.
    """
    database_url = database_queries.get_active_database_url_by_key(
        database=database, url_key=url_key
    )

    if not database_url:
        raise_not_found(request)

    database_url = crud.incremenet_database_url_clicks(
        database=database, url=database_url
    )

    return RedirectResponse(database_url.target_url)


@app.get(
    "/admin/{secret_key}", name="administration info", response_model=schemas.URLInfo
)
def get_url_info(
    secret_key: str, request: Request, database: Session = Depends(get_database)
) -> schemas.URLInfo:
    """
    The function gets the information about a URL for admin users.

    Args:
        secret_key (str): The secret key for the URL.
        request (Request): The request that was made.
        database (Session, optional): The database session. Defaults to
            Depends(get_database).

    Returns:
        schemas.URLInfo: The information about the URL.
    """
    database_url = database_queries.get_active_database_url_by_secret_key(
        database=database, secret_key=secret_key
    )

    if not database_url:
        raise_not_found(request)

    return get_admin_info(database_url)


@app.delete("/admin/{secret_key}")
def delete_url(
    secret_key: str, request: Request, database: Session = Depends(get_database)
) -> None:
    """
    The function deletes a URL from the database.

    Args:
        secret_key (str): The secret key for the URL.
        request (Request): The request that was made.
        database (Session, optional): The database session. Defaults to
            Depends(get_database).
    """
    database_url = database_queries.get_active_database_url_by_secret_key(
        database=database, secret_key=secret_key
    )

    if not database_url:
        # Not very safe as it could be used to guess the secret key.
        raise_not_found(request)

    database_url = crud.deactivate_database_url(
        database=database, database_url=database_url
    )

    return {"detail": f"URL deleted: {database_url.target_url}"}
