import pytest
from src.services.database import log_detection
from src.services.storage import upload_file
from src.services.database import get_supabase_client


def test_log_detection_inserts_to_supabase(mock_database):
    # Act: call log_detection
    result = log_detection(
        image_url="https://example.com/test.jpg",
        total=3,
        healthy=2,
        early_blight=1
    )

    # Assert: Verify that the Supabase client was called with correct data
    mock_database.table.assert_called_once_with("tomato_detections")

    # Capture what was passed to insert()
    inserted_data = mock_database.table().insert.call_args[0][0]

    assert inserted_data["total_count"] == 3
    assert inserted_data["healthy"] == 2
    assert inserted_data["early_blight"] == 1
    assert inserted_data["image_url"] == "https://example.com/test.jpg"
    assert result == [{"id": 1, "total_count": 5}]

def test_upload_file_uploads_to_r2(mock_s3_client):
    # Act: call upload_file
    upload_file("local_test_image.jpg", "device_1/test_upload.jpg")

    # Assert: Verify that boto3's upload_file was called with correct parameters
    mock_s3_client.upload_file.assert_called_once_with(
        Filename="local_test_image.jpg",
        Bucket="mock_bucket",  # Uses the TestConfig bucket name in conftest.py
        Key="device_1/test_upload.jpg"
    )

def test_get_supabase_client_success(mock_database):
        """Test successful client creation and lazy loading coverage."""
        client = get_supabase_client()
        assert client == mock_database

        # Verify client is cached (subsequent calls return the same instance)
        assert get_supabase_client() == client

def test_get_supabase_client_raises_value_error_if_missing_config(monkeypatch):
    """Test exception raising when configurations are missing."""
    from src.config import Config

    # Temporarily set Supabase credentials to None
    monkeypatch.setattr(Config, "SUPABASE_URL", None)

    with pytest.raises(ValueError, match="SUPABASE_URL and SUPABASE_PUBLISHABLE_KEY must be set."):
        get_supabase_client()
