import pytest

@pytest.fixture
def app():
    """Create a new Flask app instance with test config."""
    from src import create_app
    from src.config import Config

    class TestingConfig(Config):
        TESTING = True
        LOG_DATABASE = True

    return create_app(TestingConfig)


@pytest.fixture
def client(app):
    """Create a Flask test client"""
    with app.test_client() as client:
        yield client

@pytest.mark.parametrize("route, status_code", [
    ("/video_feed", 200),
    ("/index.html", 200),
    ("/", 200),
    ("/historical_images.html", 200),
    ("/notifications.html", 200),
    ("/statistics.html", 200),
    ("/fake_route.html", 404),
])
def test_route_get(client, route, status_code):
    """Test that the routes respond with the correct status code."""
    response = client.get(route)
    assert response.status_code == status_code

@pytest.mark.parametrize("route", [
    ("/video_feed"),
    ("/index.html"),
    ("/"),
    ("/historical_images.html"),
    ("/notifications.html"),
    ("/statistics.html"),
])
def test_route_post(client, route):
    """Test that I can only get from endpoints"""
    response = client.post(route)
    assert response.status_code == 405
