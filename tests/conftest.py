import os
import sys

os.environ.setdefault("CLOUDFLARE_BUCKET_NAME", "mock_bucket")
os.environ.setdefault("SUPABASE_URL", "https://mock.supabase.co")
os.environ.setdefault("SUPABASE_PUBLISHABLE_KEY", "mock_key")
os.environ.setdefault("CLOUDFLARE_R2_ENDPOINT", "https://mock.r2.cloudflare.com")
os.environ.setdefault("CLOUDFLARE_R2_ACCESS_KEY_ID", "mock_id")
os.environ.setdefault("CLOUDFLARE_R2_SECRET_ACCESS_KEY", "mock_secret")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def reset_globals():
    """Reset global singletons in database.py and camera.py between tests for isolation."""
    import src.services.database
    import src.services.camera

    src.services.database._supabase_client = None
    src.services.camera._model = None
    src.services.camera._camera = None
    yield
    src.services.database._supabase_client = None
    src.services.camera._model = None
    src.services.camera._camera = None


@pytest.fixture(scope="session", autouse=True)
def mock_dependencies():
    """Mock heavy external dependencies before importing the Flask app."""
    # Setup and start patchers

    mock_sentry = patch("sentry_sdk.init").start()

    # Configure OpenCV mock
    mock_cv2 = patch("cv2.VideoCapture").start()
    mock_cap = MagicMock()
    mock_cap.isOpened.return_value = True
    mock_cap.read.return_value = (True, MagicMock())
    mock_cv2.return_value = mock_cap

    # Configure cv2.imencode mock to return success and a mock buffer
    mock_imencode = patch("cv2.imencode").start()
    mock_buffer = MagicMock()
    mock_buffer.tobytes.return_value = b"mock_frame_bytes"
    mock_imencode.return_value = (True, mock_buffer)

    # Configure YOLO mock
    mock_yolo_class = patch("ultralytics.YOLO").start()
    mock_yolo_cam_class = patch("src.services.camera.YOLO").start()

    for mock_cls in (mock_yolo_class, mock_yolo_cam_class):
        mock_cls.return_value.names = {
            0: "early_blight",
            1: "healthy",
            2: "late_blight",
            3: "leaf_miner",
            4: "leaf_mold",
            5: "mosaic_virus",
            6: "septoria",
            7: "spider_mites",
            8: "yellow_leaf_curl_virus",
        }
        mock_cls.return_value.predict.return_value = []

    yield

    # Clean up patchers
    patch.stopall()


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


@pytest.fixture
def mock_s3_client():
    """Mock the boto3 S3/R2 client."""
    mock_client = MagicMock()

    # Patch the get_s3_client function in the storage service
    with patch("src.services.storage.get_s3_client", return_value=mock_client):
        yield mock_client


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
