"""
test_role_selection.py — Appium test cases for Role Selection screen.
TC021 – TC030
"""

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def find(driver, aid):
    return WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, aid))
    )


def login(driver):
    find(driver, "email_field").send_keys("organizer@test.com")
    find(driver, "password_field").send_keys("Test@1234")
    find(driver, "login_button").click()


class TestRoleSelection:

    # TC021
    def test_role_selection_screen_loads(self, driver):
        """TC021 – Role Selection screen loads after successful login."""
        login(driver)
        assert find(driver, "role_selection_screen").is_displayed()

    # TC022
    def test_organizer_role_option_present(self, driver):
        """TC022 – Organizer role option is visible on Role Selection screen."""
        login(driver)
        assert find(driver, "role_organizer").is_displayed()

    # TC023
    def test_attendee_role_option_present(self, driver):
        """TC023 – Attendee role option is visible on Role Selection screen."""
        login(driver)
        assert find(driver, "role_attendee").is_displayed()

    # TC024
    def test_volunteer_role_option_present(self, driver):
        """TC024 – Volunteer role option is visible on Role Selection screen."""
        login(driver)
        assert find(driver, "role_volunteer").is_displayed()

    # TC025
    def test_select_organizer_navigates_to_dashboard(self, driver):
        """TC025 – Selecting Organizer role navigates to Organizer Dashboard."""
        login(driver)
        find(driver, "role_organizer").click()
        assert find(driver, "organizer_dashboard_screen").is_displayed()

    # TC026
    def test_select_attendee_navigates_to_dashboard(self, driver):
        """TC026 – Selecting Attendee role navigates to Attendee Dashboard."""
        login(driver)
        find(driver, "role_attendee").click()
        assert find(driver, "attendee_dashboard_screen").is_displayed()

    # TC027
    def test_select_volunteer_navigates_to_dashboard(self, driver):
        """TC027 – Selecting Volunteer role navigates to Volunteer Dashboard."""
        login(driver)
        find(driver, "role_volunteer").click()
        assert find(driver, "volunteer_dashboard_screen").is_displayed()

    # TC028
    def test_role_selection_screen_ui_elements(self, driver):
        """TC028 – All UI elements are correctly displayed on Role Selection screen."""
        login(driver)
        assert find(driver, "role_selection_title").is_displayed()
        assert find(driver, "role_organizer").is_displayed()
        assert find(driver, "role_attendee").is_displayed()
        assert find(driver, "role_volunteer").is_displayed()

    # TC029
    def test_role_selection_screen_title(self, driver):
        """TC029 – Role Selection screen title text is correct."""
        login(driver)
        title = find(driver, "role_selection_title")
        assert "role" in title.text.lower() or "select" in title.text.lower()

    # TC030
    def test_back_button_on_role_selection(self, driver):
        """TC030 – Back button on Role Selection navigates back to Login screen."""
        login(driver)
        find(driver, "role_selection_screen").is_displayed()
        driver.back()
        assert find(driver, "login_button").is_displayed()
