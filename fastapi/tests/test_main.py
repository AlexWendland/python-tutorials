from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shortener_app.main import app, get_database
from shortener_app.models import URL

# create an in-memory SQLite database for testing
engine = create_engine("sqlite:///:memory:")
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# set up the database
def setup_function():
    get_database.session_base.metadata.create_all(bind=engine)


# tear down the database
def teardown_function():
    get_database.session_base.metadata.drop_all(bind=engine)


# create a test client for the API
client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "OpenAPI docs can be found at" in response.text


def test_process_new_url():
    # Test creating a new URL
    url = {"target_url": "http://www.example.com"}
    response = client.post("/url", json=url)
    assert response.status_code == 200
    data = response.json()
    assert data["target_url"] == url["target_url"]
    assert data["is_active"] == True
    assert data["clicks"] == 0
    assert "admin_url" in data
    assert "url" in data

    # Test creating a new URL with an invalid URL
    url = {"target_url": "not_a_url"}
    response = client.post("/url", json=url)
    assert response.status_code == 400


def test_forward_to_target_url():
    # Test forwarding to an existing URL
    url = URL(target_url="http://www.example.com")
    get_database.add(url)
    get_database.commit()
    response = client.get(f"/{url.key}")
    assert response.status_code == 307
    assert response.headers["location"] == url.target_url

    # Test forwarding to a non-existent URL
    response = client.get("/not_a_key")
    assert response.status_code == 404


def test_get_url_info():
    # Test getting info for an existing URL
    url = URL(target_url="http://www.example.com", secret_key="secret")
    get_database.add(url)
    get_database.commit()
    response = client.get(f"/admin/{url.secret_key}")
    assert response.status_code == 200
    data = response.json()
    assert data["target_url"] == url.target_url
    assert data["is_active"] == True
    assert data["clicks"] == 0
    assert "admin_url" in data
    assert "url" in data

    # Test getting info for a non-existent URL
    response = client.get("/admin/not_a_key")
    assert response.status_code == 404


def test_delete_url():
    # Test deleting an existing URL
    url = URL(target_url="http://www.example.com", secret_key="secret")
    get_database.add(url)
    get_database.commit()
    response = client.delete(f"/admin/{url.secret_key}")
    assert response.status_code == 200
    data = response.json()
    assert "URL deleted" in data["detail"]
    assert not get_database.query(URL).filter_by(id=url.id).first().is_active

    # Test deleting a non-existent URL
    response = client.delete("/admin/not_a_key")
    assert response.status_code == 404
