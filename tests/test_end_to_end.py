import re
import pytest
from playwright.sync_api import Page, expect
import subprocess
import sys


from flask.sessions import SecureCookieSessionInterface
from src import create_app

app_instance = create_app()

def generate_flask_session_cookie(username="user", user_id=1):
    serializer = SecureCookieSessionInterface().get_signing_serializer(app_instance)
    return serializer.dumps({"username": username, "user_id": user_id})

import time
import urllib.request

@pytest.fixture(scope="module", autouse=True)
def wsgi_server_configuration():
    process = subprocess.Popen([sys.executable, "wsgi.py"])

    # Wait for the server to spin up and listen on port 5000 before yielding
    timeout = 15
    start_time = time.time()
    server_ready = False

    while time.time() - start_time < timeout:
        try:
            with urllib.request.urlopen("http://127.0.0.1:5000", timeout=1) as response:
                if response.status in (200, 302, 404):
                    server_ready = True
                    break
        except Exception:
            time.sleep(0.5)

    if not server_ready:
        process.terminate()
        raise RuntimeError("wsgi.py server failed to start on port 5000 within timeout.")

    yield process

    process.terminate()

    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()


@pytest.fixture(scope="function", autouse=True)
def mock_auth_apis(page: Page):
    cookie_val = generate_flask_session_cookie("user", 1)

    def handle_auth(route):
        route.fulfill(
            status=302,
            headers={
                "Location": "http://localhost:5000/index.html",
                "Set-Cookie": f"session={cookie_val}; Path=/"
            }
        )

    page.route("**/api/login", handle_auth)
    page.route("**/api/signup", handle_auth)

@pytest.fixture(scope="function", autouse=True)
def goto_localhost_5000(page: Page):
    page.goto("http://localhost:5000")
    return

def test_has_title(page: Page):
    
    expect(page).to_have_title(re.compile("Tomato Detection Stream"))

def test_redirect(page: Page):
    expect(page).to_have_url("http://localhost:5000/login.html")

def test_user_login(page: Page) -> None:
    page.get_by_role("textbox", name="Enter Username").click()
    page.get_by_role("textbox", name="Enter Username").fill("user")
    page.get_by_role("textbox", name="Enter Password").click()
    page.get_by_role("textbox", name="Enter Password").fill("pass")
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url("http://localhost:5000/index.html")
    

def test_user_signup(page: Page) -> None:
    page.get_by_role("button", name="Sign up").click()
    page.get_by_role("textbox", name="Enter Username").click()
    page.get_by_role("textbox", name="Enter Username").fill("user5")
    page.get_by_role("textbox", name="Enter Email").click()
    page.get_by_role("textbox", name="Enter Email").fill("email")
    page.get_by_role("textbox", name="Enter Password").click()
    page.get_by_role("textbox", name="Enter Password").fill("pass")
    page.get_by_role("textbox", name="Repeat Password").click()
    page.get_by_role("textbox", name="Repeat Password").fill("pass")
    page.get_by_role("button", name="Sign Up").click()
    expect(page).to_have_url("http://localhost:5000/index.html")

def test_navigation(page: Page) -> None:
    page.get_by_role("textbox", name="Enter Username").click()
    page.get_by_role("textbox", name="Enter Username").fill("user")
    page.get_by_role("textbox", name="Enter Password").click()
    page.get_by_role("textbox", name="Enter Password").fill("pass")
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url("http://localhost:5000/index.html")
    page.get_by_role("link", name="Historical Images").click()
    expect(page).to_have_url("http://localhost:5000/historical_images.html")
    page.get_by_role("link", name="Notifications").click()
    expect(page).to_have_url("http://localhost:5000/notifications.html")
    page.get_by_role("link", name="Statistics Dashboard").click()
    expect(page).to_have_url("http://localhost:5000/statistics.html")
