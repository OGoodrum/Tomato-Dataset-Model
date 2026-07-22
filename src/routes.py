from flask import Blueprint, Response, render_template

from src.services.camera import generate_frames

bp = Blueprint("main", __name__)


@bp.route("/", methods=['GET'])
@bp.route("/index.html", methods=['GET'])
def index():
    """Video streaming home page."""
    return render_template("index.html")


@bp.route("/historical_images.html", methods=['GET'])
def historical_images():
    """Historical images page."""
    return render_template("historical_images.html")


@bp.route("/notifications.html", methods=['GET'])
def live_videos():
    """Notifications page."""
    return render_template("notifications.html", methods=["GET"])


@bp.route("/statistics.html", methods=['GET'])
def statistics():
    """Statistics page."""
    return render_template("statistics.html")


@bp.route("/video_feed", methods=['GET'])
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )
