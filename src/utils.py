from functools import wraps

from flask import make_response, request, current_app, render_template

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == current_app.config.get("SITE_USER") and auth.password == current_app.config.get("SITE_PASS"):
            return f(*args, **kwargs)
        response = make_response(render_template("/access_denied.html"), 401)
        response.headers['WWW-Authenticate'] = 'Basic realm="Login required!"'
        return response

    return decorated