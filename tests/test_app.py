def test_video_feed_route(client):
    """Test that the video feed route responds with success."""
    response = client.get("/video_feed")
    assert response.status_code == 200


def test_index_route(client):
    """Test that the index route responds with success."""
    response = client.get("/index.html")
    assert response.status_code == 200


def test_default_route(client):
    """Test that the default route responds with success."""
    response = client.get("/")
    assert response.status_code == 200


def test_historical_images_route(client):
    """Test that the historical images route responds with success."""
    response = client.get("historical_images.html")
    assert response.status_code == 200


def test_notifications_route(client):
    """Test that the notifications route responds with success."""
    response = client.get("notifications.html")
    assert response.status_code == 200


def test_statistics_route(client):
    """Test that the statistics route responds with success."""
    response = client.get("statistics.html")
    assert response.status_code == 200


def test_route_not_found(client):
    """Test that the fake route responds with failure."""
    response = client.get("fake_route.html")
    assert response.status_code == 404
