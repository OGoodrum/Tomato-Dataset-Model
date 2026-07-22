import pytest
from src.services.database import log_detection, get_supabase_client
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_database():
    """Mock the Supabase client and query builder chain."""
    mock_client = MagicMock()
    mock_table = MagicMock()
    mock_insert = MagicMock()
    mock_execute = MagicMock()

    # Chain mock methods: client.table().insert().execute()
    mock_client.table.return_value = mock_table
    mock_table.insert.return_value = mock_insert
    mock_insert.execute.return_value = mock_execute

    # Set mock payload returned by execute()
    mock_execute.data = [{"id": 1, "total_count": 5}]

    # Patch the get_supabase_client function in the database service
    with patch("src.services.database.create_client", return_value=mock_client):
        yield mock_client

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