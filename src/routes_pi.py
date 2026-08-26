from flask import Blueprint, Response

from src.services.camera import generate_frames

bp = Blueprint("main", __name__)


@bp.route("/video_feed/<camera_index>", methods=["GET"])
def video_feed(camera_index):
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(
        generate_frames(int(camera_index)), mimetype="multipart/x-mixed-replace; boundary=frame"
    )