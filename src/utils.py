from functools import wraps

from flask import make_response, request, current_app, render_template

from src.services.database import get_supabase_client

def auth_required(f):


    @wraps(f)
    def decorated(*args, **kwargs):

        auth = request.authorization

        db_client = get_supabase_client()
        response = None

        try:
            if auth and auth.username and auth.password:
                response = db_client.table("users").select('username, password').eq("username", auth.username).execute()
                print(response)
        except Exception as e:
            print(f"[DB] Error querying Supabase: {e}")
            return make_response(f"<h1>Database error {e}</h1>", 500)

        
            
        if auth and response and len(response.data) > 0 and response.data[0]["password"] == auth.password:
            return f(*args, **kwargs)
        response = make_response(render_template("/access_denied.html"), 401)
        response.headers['WWW-Authenticate'] = 'Basic realm="Login required!"'
        return response

    return decorated