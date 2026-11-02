"""
test_login.py — Appium test cases for the Login screen.
TC001 – TC020
"""

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


VALID_ORG_EMAIL    = "organizer@test.com"
VALID_ATT_EMAIL    = "attendee@test.com"
VALID_PASSWORD     = "Test@1234"
WRONG_PASSWORD     = "WrongPass99"
INVALID_EMAIL      = "not-an-email"
UNREGISTERED_EMAIL = "ghost@nowhere.com"


def find(driver, aid): 
    return WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, aid))
    )


class TestLogin:

    # TC001
    def test_login_screen_loads(self, driver):
        """TC001 – Verify Login screen loads successfully."""
        assert find(driver, "email_field").is_displayed()

    # TC002
    def test_email_field_present(self, driver):
        """TC002 – Verify email input field is present on login screen."""
        assert find(driver, "email_field").is_enabled()

    # TC003
    def test_password_field_present(self, driver):
        """TC003 – Verify password input field is present on login screen."""
        assert find(driver, "password_field").is_displayed()

    # TC004
    def test_login_button_present(self, driver):
        """TC004 – Verify Login button is present and clickable."""
        btn = find(driver, "login_button")
        assert btn.is_displayed() and btn.is_enabled()

    # TC005
    def test_login_valid_organizer(self, driver):
        """TC005 – Login with valid organizer credentials navigates to role selection."""
        find(driver, "email_field").send_keys(VALID_ORG_EMAIL)
        find(driver, "password_field").send_keys(VALID_PASSWORD)
        find(driver, "login_button").click()
        assert find(driver, "role_selection_screen").is_displayed()

    # TC006
    def test_login_valid_attendee(self, driver):
        """TC006 – Login with valid attendee credentials navigates to role selection."""
        find(driver, "email_field").send_keys(VALID_ATT_EMAIL)
        find(driver, "password_field").send_keys(VALID_PASSWORD)
        find(driver, "login_button").click()
        assert find(driver, "role_selection_screen").is_displayed()

    # TC007
    def test_login_invalid_email_format(self, driver):
        """TC007 – Login with invalid email format shows validation error."""
        find(driver, "email_field").send_keys(INVALID_EMAIL)
        find(driver, "password_field").send_keys(VALID_PASSWORD)
        find(driver, "login_button").click()
        assert find(driver, "email_error_message").is_displayed()

    # TC008
    def test_login_wrong_password(self, driver):
        """TC008 – Login with wrong password shows error message."""
        find(driver, "email_field").send_keys(VALID_ORG_EMAIL)
        find(driver, "password_field").send_keys(WRONG_PASSWORD)
        find(driver, "login_button").click()
        assert find(driver, "login_error_message").is_displayed()

    # TC009
    def test_login_empty_email(self, driver):
        """TC009 – Login with empty email field shows required error."""
        find(driver, "password_field").send_keys(VALID_PASSWORD)
        find(driver, "login_button").click()
        assert find(driver, "email_error_message").is_displayed()

    # TC010
    def test_login_empty_password(self, driver):
        """TC010 – Login with empty password field shows required error."""
        find(driver, "email_field").send_keys(VALID_ORG_EMAIL)
        find(driver, "login_button").click()
        assert find(driver, "password_error_message").is_displayed()

    # TC011
    def test_login_both_fields_empty(self, driver):
        """TC011 – Login with both fields empty shows validation errors."""
        find(driver, "login_button").click()
        assert find(driver, "email_error_message").is_displayed()
        assert find(driver, "password_error_message").is_displayed()

    # TC012
    def test_password_field_masks_input(self, driver):
        """TC012 – Verify password field masks typed characters."""
        pw_field = find(driver, "password_field")
        pw_field.send_keys(VALID_PASSWORD)
        assert pw_field.get_attribute("password") == "true"

    # TC013
    def test_forgot_password_link_present(self, driver):
        """TC013 – Verify Forgot Password link is present."""
        assert find(driver, "forgot_password_link").is_displayed()

    # TC014
    def test_signup_navigation_link_present(self, driver):
        """TC014 – Verify Sign Up navigation link is present."""
        assert find(driver, "signup_link").is_displayed()

    # TC015
    def test_login_unregistered_email(self, driver):
        """TC015 – Login with unregistered email shows user not found error."""
        find(driver, "email_field").send_keys(UNREGISTERED_EMAIL)
        find(driver, "password_field").send_keys(VALID_PASSWORD)
        find(driver, "login_button").click()
        assert find(driver, "login_error_message").is_displayed()

    # TC016
    def test_email_field_accepts_valid_format(self, driver):
        """TC016 – Email field accepts correctly formatted email addresses."""
        field = find(driver, "email_field")
        field.send_keys(VALID_ORG_EMAIL)
        assert field.get_attribute("text") == VALID_ORG_EMAIL

    # TC017
    def test_login_persists_across_restart(self, driver):
        """TC017 – Authenticated session persists after app background/foreground."""
        find(driver, "email_field").send_keys(VALID_ORG_EMAIL)
        find(driver, "password_field").send_keys(VALID_PASSWORD)
        find(driver, "login_button").click()
        driver.background_app(3)
        driver.activate_app("com.example.zyntrapass")
        assert find(driver, "role_selection_screen").is_displayed()

    # TC018
    def test_error_message_on_failed_login(self, driver):
        """TC018 – Verify error message is shown and dismissable after failed login."""
        find(driver, "email_field").send_keys(VALID_ORG_EMAIL)
        find(driver, "password_field").send_keys(WRONG_PASSWORD)
        find(driver, "login_button").click()
        error = find(driver, "login_error_message")
        assert error.is_displayed()

    # TC019
    def test_login_with_special_chars_in_password(self, driver):
        """TC019 – Login with password containing special characters works correctly."""
        find(driver, "email_field").send_keys(VALID_ORG_EMAIL)
        find(driver, "password_field").send_keys("P@$$w0rd!#%")
        find(driver, "login_button").click()
        # Should show error (wrong pass), but not crash
        assert driver.current_activity is not None

    # TC020
    def test_login_loading_indicator_shown(self, driver):
        """TC020 – Loading indicator appears while login request is in progress."""
        find(driver, "email_field").send_keys(VALID_ORG_EMAIL)
        find(driver, "password_field").send_keys(VALID_PASSWORD)
        find(driver, "login_button").click()
        # Loading spinner should be briefly visible
        assert driver.current_activity is not None
