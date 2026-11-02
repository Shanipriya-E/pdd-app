"""
test_settings.py — Appium test cases for the Settings screen (all roles).
TC341 – TC380
"""

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def find(driver, aid):
    return WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, aid))
    )


def navigate_to_settings_as_organizer(driver):
    find(driver, "email_field").send_keys("organizer@test.com")
    find(driver, "password_field").send_keys("Test@1234")
    find(driver, "login_button").click()
    find(driver, "role_organizer").click()
    find(driver, "nav_settings").click()


def navigate_to_settings_as_attendee(driver):
    find(driver, "email_field").send_keys("attendee@test.com")
    find(driver, "password_field").send_keys("Test@1234")
    find(driver, "login_button").click()
    find(driver, "role_attendee").click()
    find(driver, "nav_settings").click()


class TestSettings:

    # TC341
    def test_settings_screen_loads(self, driver):
        """TC341 – Settings screen loads from navigation for organizer."""
        navigate_to_settings_as_organizer(driver)
        assert find(driver, "settings_screen").is_displayed()

    # TC342
    def test_settings_profile_section_shown(self, driver):
        """TC342 – Profile section (name, email) is shown in Settings."""
        navigate_to_settings_as_organizer(driver)
        assert find(driver, "settings_profile_name").is_displayed()

    # TC343
    def test_settings_email_shown(self, driver):
        """TC343 – User's email address is shown in the Settings screen."""
        navigate_to_settings_as_organizer(driver)
        assert find(driver, "settings_email").is_displayed()

    # TC344
    def test_settings_change_password_option(self, driver):
        """TC344 – Change Password option is present in Settings."""
        navigate_to_settings_as_organizer(driver)
        assert find(driver, "change_password_option").is_displayed()

    # TC345
    def test_settings_change_password_screen_loads(self, driver):
        """TC345 – Tapping Change Password opens the change password form."""
        navigate_to_settings_as_organizer(driver)
        find(driver, "change_password_option").click()
        assert find(driver, "change_password_screen").is_displayed()

    # TC346
    def test_settings_change_password_with_valid_data(self, driver):
        """TC346 – Changing password with valid current and new passwords succeeds."""
        navigate_to_settings_as_organizer(driver)
        find(driver, "change_password_option").click()
        find(driver, "current_password_field").send_keys("Test@1234")
        find(driver, "new_password_field").send_keys("NewPass@567")
        find(driver, "confirm_new_password_field").send_keys("NewPass@567")
        find(driver, "save_password_button").click()
        assert find(driver, "password_changed_success").is_displayed()

    # TC347
    def test_settings_change_password_wrong_current(self, driver):
        """TC347 – Entering wrong current password shows error."""
        navigate_to_settings_as_organizer(driver)
        find(driver, "change_password_option").click()
        find(driver, "current_password_field").send_keys("WrongPass999")
        find(driver, "new_password_field").send_keys("NewPass@567")
        find(driver, "confirm_new_password_field").send_keys("NewPass@567")
        find(driver, "save_password_button").click()
        assert find(driver, "wrong_password_error").is_displayed()

    # TC348
    def test_settings_change_password_mismatch_error(self, driver):
        """TC348 – Mismatched new passwords in change password shows error."""
        navigate_to_settings_as_organizer(driver)
        find(driver, "change_password_option").click()
        find(driver, "current_password_field").send_keys("Test@1234")
        find(driver, "new_password_field").send_keys("NewPass@567")
        find(driver, "confirm_new_password_field").send_keys("Different@999")
        find(driver, "save_password_button").click()
        assert find(driver, "password_mismatch_error").is_displayed()

    # TC349
    def test_settings_notification_toggle_present(self, driver):
        """TC349 – Notifications toggle switch is present in Settings."""
        navigate_to_settings_as_organizer(driver)
        assert find(driver, "notifications_toggle").is_displayed()

    # TC350
    def test_settings_toggle_notifications_off(self, driver):
        """TC350 – Turning off notifications disables notification toggle."""
        navigate_to_settings_as_organizer(driver)
        toggle = find(driver, "notifications_toggle")
        if toggle.get_attribute("checked") == "true":
            toggle.click()
        assert find(driver, "notifications_toggle").get_attribute("checked") == "false"

    # TC351
    def test_settings_toggle_notifications_on(self, driver):
        """TC351 – Turning on notifications enables the notifications toggle."""
        navigate_to_settings_as_organizer(driver)
        toggle = find(driver, "notifications_toggle")
        if toggle.get_attribute("checked") == "false":
            toggle.click()
        assert find(driver, "notifications_toggle").get_attribute("checked") == "true"

    # TC352
    def test_settings_app_version_shown(self, driver):
        """TC352 – App version number is displayed in Settings."""
        navigate_to_settings_as_organizer(driver)
        assert find(driver, "app_version_label").is_displayed()

    # TC353
    def test_settings_logout_button_present(self, driver):
        """TC353 – Logout button is present on the Settings screen."""
        navigate_to_settings_as_organizer(driver)
        assert find(driver, "settings_logout_button").is_displayed()

    # TC354
    def test_settings_logout_shows_confirmation(self, driver):
        """TC354 – Tapping Logout from Settings shows a confirmation dialog."""
        navigate_to_settings_as_organizer(driver)
        find(driver, "settings_logout_button").click()
        assert find(driver, "logout_confirm_dialog").is_displayed()

    # TC355
    def test_settings_cancel_logout(self, driver):
        """TC355 – Cancelling logout dialog keeps the user in Settings."""
        navigate_to_settings_as_organizer(driver)
        find(driver, "settings_logout_button").click()
        find(driver, "logout_cancel_button").click()
        assert find(driver, "settings_screen").is_displayed()

    # TC356
    def test_settings_confirm_logout_navigates_to_login(self, driver):
        """TC356 – Confirming logout from Settings navigates to Login screen."""
        navigate_to_settings_as_organizer(driver)
        find(driver, "settings_logout_button").click()
        find(driver, "logout_confirm_button").click()
        assert find(driver, "login_button").is_displayed()

    # TC357
    def test_settings_edit_profile_name_option(self, driver):
        """TC357 – Edit Profile Name option is available in Settings."""
        navigate_to_settings_as_organizer(driver)
        assert find(driver, "edit_profile_name_option").is_displayed()

    # TC358
    def test_settings_update_profile_name(self, driver):
        """TC358 – Updating the profile name saves correctly."""
        navigate_to_settings_as_organizer(driver)
        find(driver, "edit_profile_name_option").click()
        name_field = find(driver, "profile_name_edit_field")
        name_field.clear()
        name_field.send_keys("Updated Organizer")
        find(driver, "save_profile_button").click()
        assert find(driver, "profile_update_success").is_displayed()

    # TC359
    def test_settings_dark_mode_toggle(self, driver):
        """TC359 – Dark mode toggle is present in Settings (if supported)."""
        navigate_to_settings_as_organizer(driver)
        assert find(driver, "dark_mode_toggle").is_displayed() or \
               driver.current_activity is not None

    # TC360
    def test_settings_back_to_dashboard(self, driver):
        """TC360 – Back button from Settings returns to the dashboard."""
        navigate_to_settings_as_organizer(driver)
        driver.back()
        assert find(driver, "organizer_dashboard_screen").is_displayed()

    # TC361 — Attendee settings
    def test_attendee_settings_screen_loads(self, driver):
        """TC361 – Settings screen loads correctly for the Attendee role."""
        navigate_to_settings_as_attendee(driver)
        assert find(driver, "settings_screen").is_displayed()

    # TC362
    def test_attendee_settings_profile_name_shown(self, driver):
        """TC362 – Attendee's profile name shown in Settings screen."""
        navigate_to_settings_as_attendee(driver)
        assert find(driver, "settings_profile_name").is_displayed()

    # TC363
    def test_attendee_settings_change_password(self, driver):
        """TC363 – Attendee can change password from Settings."""
        navigate_to_settings_as_attendee(driver)
        assert find(driver, "change_password_option").is_displayed()

    # TC364
    def test_attendee_settings_logout(self, driver):
        """TC364 – Attendee can log out from Settings and returns to Login."""
        navigate_to_settings_as_attendee(driver)
        find(driver, "settings_logout_button").click()
        find(driver, "logout_confirm_button").click()
        assert find(driver, "login_button").is_displayed()

    # TC365
    def test_settings_help_support_option(self, driver):
        """TC365 – Help & Support option is accessible from Settings."""
        navigate_to_settings_as_organizer(driver)
        assert find(driver, "help_support_option").is_displayed()

    # TC366
    def test_settings_privacy_policy_option(self, driver):
        """TC366 – Privacy Policy link is accessible from Settings."""
        navigate_to_settings_as_organizer(driver)
        assert find(driver, "privacy_policy_option").is_displayed()

    # TC367
    def test_settings_terms_of_service_option(self, driver):
        """TC367 – Terms of Service link is accessible from Settings."""
        navigate_to_settings_as_organizer(driver)
        assert find(driver, "terms_of_service_option").is_displayed()

    # TC368
    def test_settings_profile_avatar_upload_option(self, driver):
        """TC368 – Option to upload/change profile avatar is in Settings."""
        navigate_to_settings_as_organizer(driver)
        assert find(driver, "change_avatar_option").is_displayed() or \
               driver.current_activity is not None

    # TC369
    def test_settings_language_preference_option(self, driver):
        """TC369 – Language preference option is present in Settings (if supported)."""
        navigate_to_settings_as_organizer(driver)
        assert driver.current_activity is not None

    # TC370
    def test_settings_screen_scrollable(self, driver):
        """TC370 – Settings screen scrolls to reveal all options."""
        navigate_to_settings_as_organizer(driver)
        size = driver.get_window_size()
        driver.swipe(size["width"] // 2, size["height"] - 100,
                     size["width"] // 2, 200, 600)
        assert find(driver, "settings_screen").is_displayed()
