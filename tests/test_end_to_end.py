import re
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function", autouse=True)
def goto_localhost_5000(page: Page):
    page.goto("http://localhost:5000")

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
     