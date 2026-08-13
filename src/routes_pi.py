from flask import Blueprint, Response

from src.services.camera import generate_frames

bp = Blueprint("main", __name__)

@bp.route("/video_feed")
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )