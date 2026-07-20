import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture(scope="session", autouse=True)
def mock_dependencies():
    """Mock heavy external dependencies before importing the Flask app."""
    # Setup and start patchers
    mock_cv2 = patch("cv2.VideoCapture").start()
    mock_yolo = patch("ultralytics.YOLO").start()
    mock_supabase = patch("supabase.create_client").start()
    mock_boto3 = patch("boto3.client").start()
    mock_sentry = patch("sentry_sdk.init").start()
    
    # Configure OpenCV mock
    mock_cap = MagicMock()
    mock_cap.isOpened.return_value = True
    mock_cap.read.return_value = (True, MagicMock())
    mock_cv2.return_value = mock_cap

    # Configure YOLO mock
    mock_yolo.return_value.names = {
        0: "early_blight", 1: "healthy", 2: "late_blight", 3: "leaf_miner",
        4: "leaf_mold", 5: "mosaic_virus", 6: "septoria", 7: "spider_mites",
        8: "yellow_leaf_curl_virus"
    }

    yield

    # Clean up patchers
    patch.stopall()

@pytest.fixture
def client():
    """Create a Flask test client."""
    # We import app here so that the patches in mock_dependencies are active
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

