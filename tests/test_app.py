def test_video_feed_route(client):
    """Test that the video feed route responds with success."""
    response = client.get("/video_feed")
    assert response.status_code == 200