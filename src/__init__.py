import os

import sentry_sdk
from flask import Flask
from flask_cors import CORS

from src.config import Config


def create_app(config_class=Config, device_type=None):
    device_type = device_type or os.environ.get("DEVICE_TYPE", "pi")

    src_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(src_dir, 'templates')
    static_dir = os.path.join(src_dir, 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(config_class)
    if app.config.get("SENTRY_DSN"):
        sentry_sdk.init(
            dsn=app.config["SENTRY_DSN"],
            send_default_pii=True,
            enable_logs=True,
            traces_sample_rate=1.0,
            profile_session_sample_rate=1.0,
        )

    CORS(app, resources={r"/video_feed": {"origins": ""}})

    if device_type == "server":
        from src.routes_server import bp as main_bp
    elif device_type == "pi":
        from src.routes_pi import bp as main_bp
    app.register_blueprint(main_bp)

    if os.environ.get("WERKZEUG_RUN_MAIN") != "false":
        if app.config.get("LOG_DATABASE"):
            from src.services.camera import start_background_logger
            start_background_logger()

    return app
