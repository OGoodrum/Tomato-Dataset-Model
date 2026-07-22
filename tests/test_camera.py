import pytest
from src.services.camera import generate_frames


def test_generate_frames():
    """Test that generate_frames yields formatted MJPEG frame bytes."""
    gen = generate_frames()
    frame = next(gen)
    assert b"--frame" in frame
    assert b"Content-Type: image/jpeg" in frame
    assert b"mock_frame_bytes" in frame
    gen.close()


def test_generate_frames_camera_not_open(monkeypatch):
    """Test generate_frames early exit when camera fails to open."""
    from unittest.mock import MagicMock
    import src.services.camera as camera_mod

    mock_cap = MagicMock()
    mock_cap.isOpened.return_value = False
    monkeypatch.setattr(camera_mod, "get_camera", lambda: mock_cap)

    gen = camera_mod.generate_frames()
    with pytest.raises(StopIteration):
        next(gen)


def test_generate_frames_read_failure(monkeypatch):
    """Test generate_frames exit when frame read fails."""
    from unittest.mock import MagicMock
    import src.services.camera as camera_mod

    mock_cap = MagicMock()
    mock_cap.isOpened.return_value = True
    mock_cap.read.return_value = (False, None)
    monkeypatch.setattr(camera_mod, "get_camera", lambda: mock_cap)

    gen = camera_mod.generate_frames()
    with pytest.raises(StopIteration):
        next(gen)
