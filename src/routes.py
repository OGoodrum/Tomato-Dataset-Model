from flask import Blueprint, Response, render_template, request, session, jsonify, url_for, redirect
from flask_bcrypt import Bcrypt

from src.services.camera import generate_frames
from src.services.database import get_supabase_client

from .utils import auth_required

bp = Blueprint("main", __name__)
bcrypt = Bcrypt()


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
    user = session.get("username")
    db_client = get_supabase_client()

    
    try:
        response = (
            db_client.from_('tomato_detections')
            .select('created_at, image_url, devices!inner(name, location, users!owner!inner(username))')
            .eq('devices.users.username', user)
            .order("created_at", desc=True)
            .execute()
        )
        image_data = response.data
    except Exception as e:
        image_data = []
        print(f"error {e}")
    return render_template("historical_images.html", image_data=image_data)


@bp.route("/notifications.html")
@auth_required
def live_videos():
    """Notifications page."""
    """Historical images page."""
    user = session.get("username")
    db_client = get_supabase_client()

    
    try:
        response = (
            db_client.from_('tomato_detections')
            .select('id, created_at, image_url, total_count, healthy, early_blight, late_blight, leaf_miner, leaf_mold, mosaic_virus, septoria, spider_mites, yellow_leaf_curl_virus, devices!inner(name, location, users!owner!inner(username))')
            .eq('devices.users.username', user)
            .order("created_at", desc=True)
            .execute()
        )
        notifications_data = response.data
    except Exception as e:
        notifications_data = []
        print(f"error {e}")
    
    return render_template("notifications.html", notifications_data=notifications_data)


@bp.route("/statistics.html")
@auth_required
def statistics():
    """Statistics page."""
    user = session.get("username")
    db_client = get_supabase_client()

    
    try:
        response = (
            db_client.from_('tomato_detections')
            .select('*, devices!inner(name, location, users!owner!inner(username))')
            .eq('devices.users.username', user)
            .order("created_at", desc=True)
            .execute()
        )
        statistics_data = response.data
    except Exception as e:
        statistics_data = []
        print(f"error {e}")
    return render_template("statistics.html", statistics_data=statistics_data)


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
    data = request.get_json(silent=True) or request.form
    username = data.get("uname") or data.get("username")
    password = data.get("psw") or data.get("password")

    db_client = get_supabase_client()
    try:
        response = db_client.table("users").select('id, username, password').eq("username", username).execute()
        if response.data and bcrypt.check_password_hash(response.data[0]["password"], password):
            session['username'] = username
            session['user_id'] = response.data[0]["id"]
            return redirect(url_for('main.index'))
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

    return jsonify({"success": False, "message": "Invalid username or password"}), 401

@bp.route("/login.html", methods=["GET"])
def login_page():
    return render_template("login.html")

@bp.route("/api/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('main.login_page'))

@bp.route("/signup.html", methods=["GET"])
def signup():
    return render_template("signup.html")

@bp.route("/api/signup", methods=["POST"])
def signup_api():
    """Register a new user to the database"""
    data = request.get_json(silent=True) or request.form
    username = data.get("uname") or data.get("username")
    password = data.get("psw") or data.get("password")
    email = data.get("email")

    db_client = get_supabase_client()

    try:
        response = db_client.table("users").select('username, password').eq("username", username).execute()
        if response.data and response.data[0]["username"] == username:
            return jsonify({"Success": False, "message": "Invalid username, someone already has this username"}), 401

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        response = db_client.table("users").insert({"username": username, "password": hashed_password, "email": email}).execute()
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

    print(response.data)
    session['username'] = username
    session['user_id'] = response.data[0]["id"]
    return redirect(url_for("main.index"))
