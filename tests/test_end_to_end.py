import re
import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="function", autouse=True)
def mock_signup_api(page: Page):
    page.route("**/api/signup", lambda route: route.fulfill(status=200, json={"status": "success"}))

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
