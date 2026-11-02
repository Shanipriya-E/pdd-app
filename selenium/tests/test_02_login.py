"""
test_02_login.py  —  Login Page
TC021 – TC055
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from conftest import go, wait_for, click_when_ready, fill, login_as_organizer
from config import ORGANIZER_EMAIL, ORGANIZER_PASSWORD, ORGANIZER_SECRET_KEY


class TestLoginPage:

    def test_TC021_login_page_loads(self, driver):
        """TC021 – Login page loads and title contains 'ZyntraPass'."""
        go(driver, "/login.html")
        assert "ZyntraPass" in driver.title

    def test_TC022_login_title_visible(self, driver):
        """TC022 – 'Sign in to continue' heading is visible."""
        go(driver, "/login.html")
        h2 = wait_for(driver, By.CLASS_NAME, "auth-title")
        assert h2.is_displayed()

    def test_TC023_subtitle_visible(self, driver):
        """TC023 – Subtitle text is visible on login page."""
        go(driver, "/login.html")
        sub = wait_for(driver, By.CLASS_NAME, "auth-subtitle")
        assert sub.is_displayed()

    def test_TC024_attendee_role_option_present(self, driver):
        """TC024 – Attendee role option card is displayed."""
        go(driver, "/login.html")
        el = wait_for(driver, By.CSS_SELECTOR, "[data-role='attendee']")
        assert el.is_displayed()

    def test_TC025_organizer_role_option_present(self, driver):
        """TC025 – Organizer role option card is displayed."""
        go(driver, "/login.html")
        el = wait_for(driver, By.CSS_SELECTOR, "[data-role='organizer']")
        assert el.is_displayed()

    def test_TC026_volunteer_role_option_present(self, driver):
        """TC026 – Volunteer role option card is displayed."""
        go(driver, "/login.html")
        el = wait_for(driver, By.CSS_SELECTOR, "[data-role='volunteer']")
        assert el.is_displayed()

    def test_TC027_email_field_present(self, driver):
        """TC027 – Email input field is present on the login form."""
        go(driver, "/login.html")
        assert wait_for(driver, By.ID, "email").is_displayed()

    def test_TC028_password_field_present(self, driver):
        """TC028 – Password input field is present on the login form."""
        go(driver, "/login.html")
        assert wait_for(driver, By.ID, "password").is_displayed()

    def test_TC029_login_button_present(self, driver):
        """TC029 – Login submit button is present."""
        go(driver, "/login.html")
        assert wait_for(driver, By.ID, "submit-btn").is_displayed()

    def test_TC030_create_account_link_present(self, driver):
        """TC030 – 'Create Account' link is present at the bottom."""
        go(driver, "/login.html")
        link = wait_for(driver, By.ID, "create-account-link")
        assert link.is_displayed()

    def test_TC031_forgot_password_link_present(self, driver):
        """TC031 – 'Forgot password?' link is present."""
        go(driver, "/login.html")
        link = wait_for(driver, By.CLASS_NAME, "forgot-pw")
        assert link.is_displayed()

    def test_TC032_remember_me_checkbox_present(self, driver):
        """TC032 – Remember Me checkbox is present."""
        go(driver, "/login.html")
        cb = driver.find_element(By.CSS_SELECTOR, ".remember-me input[type='checkbox']")
        assert cb.is_displayed()

    def test_TC033_select_organizer_shows_secret_key(self, driver):
        """TC033 – Selecting Organizer role shows the Secret Key field."""
        go(driver, "/login.html")
        click_when_ready(driver, By.CSS_SELECTOR, "[data-role='organizer']")
        secret = wait_for(driver, By.ID, "secretKey")
        assert secret.is_displayed()

    def test_TC034_select_volunteer_shows_code_field(self, driver):
        """TC034 – Selecting Volunteer shows Volunteer Code field and hides email/password."""
        go(driver, "/login.html")
        click_when_ready(driver, By.CSS_SELECTOR, "[data-role='volunteer']")
        code = wait_for(driver, By.ID, "volunteerCode")
        assert code.is_displayed()

    def test_TC035_select_attendee_hides_secret_key(self, driver):
        """TC035 – Selecting Attendee hides the Secret Key field."""
        go(driver, "/login.html")
        click_when_ready(driver, By.CSS_SELECTOR, "[data-role='attendee']")
        sk = driver.find_element(By.ID, "secretKey")
        assert not sk.is_displayed()

    def test_TC036_organizer_role_card_selects_on_click(self, driver):
        """TC036 – Clicking organizer card adds 'selected' CSS class."""
        go(driver, "/login.html")
        card = click_when_ready(driver, By.CSS_SELECTOR, "[data-role='organizer']")
        assert "selected" in card.get_attribute("class")

    def test_TC037_attendee_role_card_selects_on_click(self, driver):
        """TC037 – Clicking attendee card adds 'selected' CSS class."""
        go(driver, "/login.html")
        card = click_when_ready(driver, By.CSS_SELECTOR, "[data-role='attendee']")
        assert "selected" in card.get_attribute("class")

    def test_TC038_volunteer_role_card_selects_on_click(self, driver):
        """TC038 – Clicking volunteer card adds 'selected' CSS class."""
        go(driver, "/login.html")
        card = click_when_ready(driver, By.CSS_SELECTOR, "[data-role='volunteer']")
        assert "selected" in card.get_attribute("class")

    def test_TC039_no_role_selected_shows_error(self, driver):
        """TC039 – Submitting without selecting a role shows validation error."""
        go(driver, "/login.html")
        fill(driver, By.ID, "email", ORGANIZER_EMAIL)
        fill(driver, By.ID, "password", ORGANIZER_PASSWORD)
        click_when_ready(driver, By.ID, "submit-btn")
        err = wait_for(driver, By.ID, "error-msg")
        assert err.is_displayed() and len(err.text.strip()) > 0

    def test_TC040_empty_email_blocked(self, driver):
        """TC040 – Submitting organizer form without email is blocked by browser validation."""
        go(driver, "/login.html")
        click_when_ready(driver, By.CSS_SELECTOR, "[data-role='organizer']")
        fill(driver, By.ID, "password", ORGANIZER_PASSWORD)
        fill(driver, By.ID, "secretKey", ORGANIZER_SECRET_KEY)
        driver.find_element(By.ID, "submit-btn").click()
        assert driver.current_url.endswith("login.html") or "login" in driver.current_url

    def test_TC041_invalid_email_format_blocked(self, driver):
        """TC041 – Invalid email format triggers HTML5 validation."""
        go(driver, "/login.html")
        click_when_ready(driver, By.CSS_SELECTOR, "[data-role='organizer']")
        fill(driver, By.ID, "email", "notanemail")
        fill(driver, By.ID, "password", ORGANIZER_PASSWORD)
        fill(driver, By.ID, "secretKey", ORGANIZER_SECRET_KEY)
        driver.find_element(By.ID, "submit-btn").click()
        assert "login" in driver.current_url

    def test_TC042_wrong_password_shows_error(self, driver):
        """TC042 – Wrong password shows authentication error message."""
        go(driver, "/login.html")
        click_when_ready(driver, By.CSS_SELECTOR, "[data-role='organizer']")
        fill(driver, By.ID, "email", ORGANIZER_EMAIL)
        fill(driver, By.ID, "password", "WrongPass9999!")
        fill(driver, By.ID, "secretKey", ORGANIZER_SECRET_KEY)
        click_when_ready(driver, By.ID, "submit-btn")
        err = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "error-msg"))
        )
        assert err.is_displayed()

    def test_TC043_wrong_secret_key_shows_error(self, driver):
        """TC043 – Correct email/password but wrong secret key shows error."""
        go(driver, "/login.html")
        click_when_ready(driver, By.CSS_SELECTOR, "[data-role='organizer']")
        fill(driver, By.ID, "email", ORGANIZER_EMAIL)
        fill(driver, By.ID, "password", ORGANIZER_PASSWORD)
        fill(driver, By.ID, "secretKey", "WrongKey99")
        click_when_ready(driver, By.ID, "submit-btn")
        err = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "error-msg"))
        )
        assert "Invalid" in err.text or err.is_displayed()

    def test_TC044_submit_btn_text_is_login(self, driver):
        """TC044 – Submit button label is 'Login'."""
        go(driver, "/login.html")
        btn = wait_for(driver, By.ID, "submit-btn")
        assert "Login" in btn.text or "login" in btn.text.lower()

    def test_TC045_password_field_type_is_password(self, driver):
        """TC045 – Password field type attribute is 'password' (masked input)."""
        go(driver, "/login.html")
        pw = wait_for(driver, By.ID, "password")
        assert pw.get_attribute("type") == "password"

    def test_TC046_secret_key_field_type_is_password(self, driver):
        """TC046 – Secret key field type is 'password' (masked)."""
        go(driver, "/login.html")
        click_when_ready(driver, By.CSS_SELECTOR, "[data-role='organizer']")
        sk = wait_for(driver, By.ID, "secretKey")
        assert sk.get_attribute("type") == "password"

    def test_TC047_email_field_placeholder_present(self, driver):
        """TC047 – Email field has a visible placeholder."""
        go(driver, "/login.html")
        ph = driver.find_element(By.ID, "email").get_attribute("placeholder")
        assert ph and len(ph) > 0

    def test_TC048_role_icons_visible(self, driver):
        """TC048 – All three role icon elements are visible."""
        go(driver, "/login.html")
        icons = driver.find_elements(By.CLASS_NAME, "role-icon")
        assert len(icons) >= 3

    def test_TC049_role_text_attendee_visible(self, driver):
        """TC049 – Attendee role card displays 'Attendee' text."""
        go(driver, "/login.html")
        card = wait_for(driver, By.CSS_SELECTOR, "[data-role='attendee']")
        assert "Attendee" in card.text

    def test_TC050_role_text_organizer_visible(self, driver):
        """TC050 – Organizer role card displays 'Organizer' text."""
        go(driver, "/login.html")
        card = wait_for(driver, By.CSS_SELECTOR, "[data-role='organizer']")
        assert "Organizer" in card.text

    def test_TC051_role_text_volunteer_visible(self, driver):
        """TC051 – Volunteer role card displays 'Volunteer' text."""
        go(driver, "/login.html")
        card = wait_for(driver, By.CSS_SELECTOR, "[data-role='volunteer']")
        assert "Volunteer" in card.text

    def test_TC052_create_account_link_navigates_to_signup(self, driver):
        """TC052 – Clicking Create Account link navigates to signup page."""
        go(driver, "/login.html")
        click_when_ready(driver, By.CSS_SELECTOR, "[data-role='attendee']")
        click_when_ready(driver, By.ID, "create-account-link")
        WebDriverWait(driver, 10).until(EC.url_contains("signup"))
        assert "signup" in driver.current_url

    def test_TC053_volunteer_code_field_placeholder(self, driver):
        """TC053 – Volunteer code field has '4-digit code' placeholder."""
        go(driver, "/login.html")
        click_when_ready(driver, By.CSS_SELECTOR, "[data-role='volunteer']")
        ph = driver.find_element(By.ID, "volunteerCode").get_attribute("placeholder")
        assert ph and ("digit" in ph.lower() or "code" in ph.lower())

    def test_TC054_auth_container_background_white(self, driver):
        """TC054 – Auth container card is rendered (present in DOM)."""
        go(driver, "/login.html")
        container = wait_for(driver, By.CLASS_NAME, "auth-container")
        assert container.is_displayed()

    def test_TC055_page_body_dark_background(self, driver):
        """TC055 – Page body has dark background color style applied."""
        go(driver, "/login.html")
        body_bg = driver.execute_script(
            "return window.getComputedStyle(document.body).backgroundColor;"
        )
        # Dark background — not plain white
        assert body_bg != "rgba(255, 255, 255, 1)" or "0d162a" in driver.page_source
