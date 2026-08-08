from functools import wraps

from flask import request, session, jsonify, redirect, url_for

def auth_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        if 'username' in session:
            return f(*args, **kwargs)

        # If unauthenticated request, redirect to login or return 401
        if request.path.startswith('/api/') or request.is_json:
            return jsonify({'error': 'Unauthorized'}), 401

        return redirect(url_for('main.login_page'))
       

    return decorated