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
    import src.services.storage

    src.services.database._supabase_client = None
    src.services.camera._model = None
    src.services.camera._camera = None
    src.services.storage._s3_client = None
    yield
    src.services.database._supabase_client = None
    src.services.camera._model = None
    src.services.camera._camera = None
    src.services.storage._s3_client = None


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
