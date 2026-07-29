from flask import Blueprint, Response, render_template, request, session, jsonify, url_for

from src.services.camera import generate_frames
from src.services.database import get_supabase_client

from .utils import auth_required

bp = Blueprint("main", __name__)


@bp.route("/")
@bp.route("/index.html")
@auth_required
def index():
    """Video streaming home page."""
    return render_template("index.html")


@bp.route("/historical_images.html")
@auth_required
def historical_images():
    """Historical images page."""
    return render_template("historical_images.html")


@bp.route("/notifications.html")
@auth_required
def live_videos():
    """Notifications page."""
    return render_template("notifications.html")


@bp.route("/statistics.html")
@auth_required
def statistics():
    """Statistics page."""
    return render_template("statistics.html")


@bp.route("/video_feed")
@auth_required
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@bp.route("/api/login", methods=["POST"])
def login_api():
    """Login route for logging in a user"""
    data = request.get_json() or request.form
    username = data.get("uname") or data.get("username")
    password = data.get("psw") or data.get("password")

    db_client = get_supabase_client()
    try:
        response = db_client.table("users").select('username, password').eq("username", username).execute()
        if response.data and response.data[0]["password"] == password:
            session['user'] = username
            return jsonify({"success": True, "redirect": url_for("main.index")})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

    return jsonify({"success": False, "message": "Invalid username or password"}), 401

@bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")