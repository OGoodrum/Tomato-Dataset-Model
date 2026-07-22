import pytest
from unittest.mock import MagicMock, patch
from src.services.storage import upload_file


@pytest.fixture
def mock_s3_client():
    """Mock the boto3 S3/R2 client."""
    mock_client = MagicMock()

    # Patch the get_s3_client function in the storage service
    with patch("src.services.storage.get_s3_client", return_value=mock_client):
        yield mock_client

def test_upload_file_uploads_to_r2(mock_s3_client):
    # Act: call upload_file
    upload_file("local_test_image.jpg", "device_1/test_upload.jpg")

    # Assert: Verify that boto3's upload_file was called with correct parameters
    mock_s3_client.upload_file.assert_called_once_with(
        Filename="local_test_image.jpg",
        Bucket="mock_bucket",  # Uses the TestConfig bucket name in conftest.py
        Key="device_1/test_upload.jpg",
    )
