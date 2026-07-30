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

@pytest.fixture
def logged_in_client(client):
    """A test client with an active authenticated user session"""
    with client.session_transaction() as sess:
        sess['user'] = 'test_user'
    return client

@pytest.mark.parametrize("route, status_code", [
    ("/video_feed", 302),
    ("/index.html", 302),
    ("/", 302),
    ("/historical_images.html", 302),
    ("/notifications.html", 302),
    ("/statistics.html", 302),
    ("/login.html", 200),
    ("/signup.html", 200),
    ("/fake_route.html", 404),
])
def test_logged_out_get(client, route, status_code):
    """Test GET method on all routes when logged out"""
    response = client.get(route)
    assert response.status_code == status_code
    

@pytest.mark.parametrize("route, status_code", [
    ("/video_feed", 200),
    ("/index.html", 200),
    ("/", 200),
    ("/historical_images.html", 200),
    ("/notifications.html", 200),
    ("/statistics.html", 200),
    ("/fake_route.html", 404),
])
def test_route_logged_in_get(logged_in_client, route, status_code):
    """Test GET method on routes when logged in."""
    response = logged_in_client.get(route)
    assert response.status_code == status_code

@pytest.mark.parametrize("route", [
    ("/video_feed"),
    ("/index.html"),
    ("/"),
    ("/historical_images.html"),
    ("/notifications.html"),
    ("/statistics.html"),
    ("/login.html"),
    ("/signup.html"),
])
def test_route_post(client, route):
    """Test that I can only get from endpoints"""
    response = client.post(route)
    assert response.status_code == 405

@pytest.mark.parametrize("route", [
    ("/video_feed"),
    ("/index.html"),
    ("/"),
    ("/historical_images.html"),
    ("/notifications.html"),
    ("/statistics.html"),
])
def test_redirect(client, route):
    """Test that if login is incorrect then the page will not load"""
    response = client.get(route)
    assert response.status_code == 302

@pytest.mark.parametrize("route", [
    ("/api/login"),
    ("/api/signup"),
])
def test_get_api_routes(client, route):
    response = client.get(route)
    assert response.status_code == 405




