"""
test_03_signup.py  —  Organizer Signup Page
TC056 – TC080
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from conftest import go, wait_for, click_when_ready, fill


class TestSignupPage:

    def test_TC056_signup_page_loads(self, driver):
        """TC056 – Signup page loads successfully."""
        go(driver, "/signup.html")
        assert "ZyntraPass" in driver.title or "Signup" in driver.title or "Create" in driver.title

    def test_TC057_signup_title_visible(self, driver):
        """TC057 – 'Create your organizer account' heading is visible."""
        go(driver, "/signup.html")
        h2 = wait_for(driver, By.CLASS_NAME, "auth-title")
        assert h2.is_displayed()

    def test_TC058_subtitle_visible(self, driver):
        """TC058 – Subtitle text is visible on signup page."""
        go(driver, "/signup.html")
        sub = wait_for(driver, By.CLASS_NAME, "auth-subtitle")
        assert sub.is_displayed()

    def test_TC059_full_name_field_present(self, driver):
        """TC059 – Full Name input field is present."""
        go(driver, "/signup.html")
        assert wait_for(driver, By.ID, "fullName").is_displayed()

    def test_TC060_email_field_present(self, driver):
        """TC060 – Email input field is present."""
        go(driver, "/signup.html")
        assert wait_for(driver, By.ID, "email").is_displayed()

    def test_TC061_phone_field_present(self, driver):
        """TC061 – Phone number input field is present."""
        go(driver, "/signup.html")
        assert wait_for(driver, By.ID, "phone").is_displayed()

    def test_TC062_institution_field_present(self, driver):
        """TC062 – Institution/College/Company field is present."""
        go(driver, "/signup.html")
        assert wait_for(driver, By.ID, "institution").is_displayed()

    def test_TC063_area_city_field_present(self, driver):
        """TC063 – Area/City field is present."""
        go(driver, "/signup.html")
        assert wait_for(driver, By.ID, "areaCity").is_displayed()

    def test_TC064_native_place_field_present(self, driver):
        """TC064 – Native Place field is present."""
        go(driver, "/signup.html")
        assert wait_for(driver, By.ID, "nativePlace").is_displayed()

    def test_TC065_secret_key_field_present(self, driver):
        """TC065 – Organizer Secret Key field is present."""
        go(driver, "/signup.html")
        assert wait_for(driver, By.ID, "secretKey").is_displayed()

    def test_TC066_password_field_present(self, driver):
        """TC066 – Password field is present."""
        go(driver, "/signup.html")
        assert wait_for(driver, By.ID, "password").is_displayed()

    def test_TC067_confirm_password_field_present(self, driver):
        """TC067 – Confirm Password field is present."""
        go(driver, "/signup.html")
        assert wait_for(driver, By.ID, "confirmPassword").is_displayed()

    def test_TC068_submit_button_present(self, driver):
        """TC068 – 'Create account' submit button is present."""
        go(driver, "/signup.html")
        btn = wait_for(driver, By.ID, "submit-btn")
        assert btn.is_displayed() and "Create" in btn.text

    def test_TC069_secret_key_banner_visible(self, driver):
        """TC069 – Important Secret Key information banner is displayed."""
        go(driver, "/signup.html")
        banner = wait_for(driver, By.CLASS_NAME, "secret-key-banner")
        assert banner.is_displayed()

    def test_TC070_upload_profile_photo_btn_visible(self, driver):
        """TC070 – 'Upload profile photo' button is visible."""
        go(driver, "/signup.html")
        btns = driver.find_elements(By.CLASS_NAME, "upload-btn")
        assert len(btns) > 0 and btns[0].is_displayed()

    def test_TC071_avatar_placeholder_visible(self, driver):
        """TC071 – Avatar placeholder ('OR') is visible."""
        go(driver, "/signup.html")
        avatar = wait_for(driver, By.CLASS_NAME, "avatar-placeholder")
        assert avatar.is_displayed()

    def test_TC072_password_field_is_masked(self, driver):
        """TC072 – Password field type is 'password' (masked)."""
        go(driver, "/signup.html")
        pw = wait_for(driver, By.ID, "password")
        assert pw.get_attribute("type") == "password"

    def test_TC073_confirm_password_field_is_masked(self, driver):
        """TC073 – Confirm Password field type is 'password' (masked)."""
        go(driver, "/signup.html")
        cp = wait_for(driver, By.ID, "confirmPassword")
        assert cp.get_attribute("type") == "password"

    def test_TC074_secret_key_is_masked(self, driver):
        """TC074 – Secret Key field type is 'password' (masked)."""
        go(driver, "/signup.html")
        sk = wait_for(driver, By.ID, "secretKey")
        assert sk.get_attribute("type") == "password"

    def test_TC075_sign_in_link_present(self, driver):
        """TC075 – 'Sign in' link is present at bottom of signup page."""
        go(driver, "/signup.html")
        link = driver.find_element(By.LINK_TEXT, "Sign in")
        assert link.is_displayed()

    def test_TC076_sign_in_link_navigates_to_login(self, driver):
        """TC076 – Clicking 'Sign in' navigates to login.html."""
        go(driver, "/signup.html")
        driver.find_element(By.LINK_TEXT, "Sign in").click()
        WebDriverWait(driver, 10).until(EC.url_contains("login"))
        assert "login" in driver.current_url

    def test_TC077_fullname_accepts_input(self, driver):
        """TC077 – Full Name field accepts typed text."""
        go(driver, "/signup.html")
        fill(driver, By.ID, "fullName", "Test Organizer")
        val = driver.find_element(By.ID, "fullName").get_attribute("value")
        assert "Test Organizer" == val

    def test_TC078_email_accepts_input(self, driver):
        """TC078 – Email field accepts typed text."""
        go(driver, "/signup.html")
        fill(driver, By.ID, "email", "test@example.com")
        val = driver.find_element(By.ID, "email").get_attribute("value")
        assert "test@example.com" == val

    def test_TC079_secret_key_banner_contains_important_text(self, driver):
        """TC079 – Secret Key banner contains 'Important' text."""
        go(driver, "/signup.html")
        banner = wait_for(driver, By.CLASS_NAME, "secret-key-banner")
        assert "Important" in banner.text or "secret" in banner.text.lower()

    def test_TC080_form_has_all_required_fields(self, driver):
        """TC080 – All required fields are marked as required in HTML."""
        go(driver, "/signup.html")
        required_ids = ["fullName", "email", "phone", "institution", "password", "confirmPassword"]
        for fid in required_ids:
            el = driver.find_element(By.ID, fid)
            req = el.get_attribute("required")
            assert req is not None, f"Field '{fid}' should be required"
