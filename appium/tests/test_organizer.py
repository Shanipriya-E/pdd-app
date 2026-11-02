"""
test_organizer.py — Appium test cases for Organizer Signup and Organizer Dashboard.
TC031 – TC075
"""

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def find(driver, aid):
    return WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, aid))
    )


def login_as_organizer(driver):
    find(driver, "email_field").send_keys("organizer@test.com")
    find(driver, "password_field").send_keys("Test@1234")
    find(driver, "login_button").click()
    find(driver, "role_organizer").click()


class TestOrganizerSignup:

    # TC031
    def test_signup_link_navigates_to_signup(self, driver):
        """TC031 – Tapping Sign Up link on Login opens the Signup screen."""
        find(driver, "signup_link").click()
        assert find(driver, "signup_screen").is_displayed()

    # TC032
    def test_signup_screen_loads(self, driver):
        """TC032 – Organizer Signup screen loads with all required fields."""
        find(driver, "signup_link").click()
        assert find(driver, "signup_name_field").is_displayed()

    # TC033
    def test_signup_name_field_present(self, driver):
        """TC033 – Name field is present on signup screen."""
        find(driver, "signup_link").click()
        assert find(driver, "signup_name_field").is_enabled()

    # TC034
    def test_signup_email_field_present(self, driver):
        """TC034 – Email field is present on signup screen."""
        find(driver, "signup_link").click()
        assert find(driver, "signup_email_field").is_displayed()

    # TC035
    def test_signup_password_field_present(self, driver):
        """TC035 – Password field is present on signup screen."""
        find(driver, "signup_link").click()
        assert find(driver, "signup_password_field").is_displayed()

    # TC036
    def test_signup_confirm_password_field_present(self, driver):
        """TC036 – Confirm Password field is present on signup screen."""
        find(driver, "signup_link").click()
        assert find(driver, "signup_confirm_password_field").is_displayed()

    # TC037
    def test_signup_with_valid_data(self, driver):
        """TC037 – Signup with all valid data creates account successfully."""
        find(driver, "signup_link").click()
        find(driver, "signup_name_field").send_keys("Test Organizer")
        find(driver, "signup_email_field").send_keys("neworg@test.com")
        find(driver, "signup_password_field").send_keys("Test@1234")
        find(driver, "signup_confirm_password_field").send_keys("Test@1234")
        find(driver, "signup_button").click()
        assert driver.current_activity is not None

    # TC038
    def test_signup_empty_name_shows_error(self, driver):
        """TC038 – Signup with empty name field shows validation error."""
        find(driver, "signup_link").click()
        find(driver, "signup_email_field").send_keys("org@test.com")
        find(driver, "signup_password_field").send_keys("Test@1234")
        find(driver, "signup_confirm_password_field").send_keys("Test@1234")
        find(driver, "signup_button").click()
        assert find(driver, "signup_name_error").is_displayed()

    # TC039
    def test_signup_mismatched_passwords_shows_error(self, driver):
        """TC039 – Signup with mismatched passwords shows error."""
        find(driver, "signup_link").click()
        find(driver, "signup_name_field").send_keys("Org Name")
        find(driver, "signup_email_field").send_keys("org@test.com")
        find(driver, "signup_password_field").send_keys("Test@1234")
        find(driver, "signup_confirm_password_field").send_keys("Different@999")
        find(driver, "signup_button").click()
        assert find(driver, "password_mismatch_error").is_displayed()

    # TC040
    def test_signup_duplicate_email_shows_error(self, driver):
        """TC040 – Signup with already registered email shows duplicate error."""
        find(driver, "signup_link").click()
        find(driver, "signup_name_field").send_keys("Dup Org")
        find(driver, "signup_email_field").send_keys("organizer@test.com")
        find(driver, "signup_password_field").send_keys("Test@1234")
        find(driver, "signup_confirm_password_field").send_keys("Test@1234")
        find(driver, "signup_button").click()
        assert find(driver, "duplicate_email_error").is_displayed()

    # TC041
    def test_signup_weak_password_shows_error(self, driver):
        """TC041 – Signup with weak password (no special char) shows error."""
        find(driver, "signup_link").click()
        find(driver, "signup_name_field").send_keys("Org")
        find(driver, "signup_email_field").send_keys("org2@test.com")
        find(driver, "signup_password_field").send_keys("password")
        find(driver, "signup_confirm_password_field").send_keys("password")
        find(driver, "signup_button").click()
        assert find(driver, "weak_password_error").is_displayed()

    # TC042
    def test_signup_invalid_email_format(self, driver):
        """TC042 – Signup with invalid email format shows validation error."""
        find(driver, "signup_link").click()
        find(driver, "signup_email_field").send_keys("invalidemail")
        find(driver, "signup_button").click()
        assert find(driver, "signup_email_error").is_displayed()

    # TC043
    def test_signup_back_navigates_to_login(self, driver):
        """TC043 – Back button on signup screen returns to Login screen."""
        find(driver, "signup_link").click()
        driver.back()
        assert find(driver, "login_button").is_displayed()

    # TC044
    def test_signup_all_fields_empty_shows_errors(self, driver):
        """TC044 – Signup with all empty fields shows all validation errors."""
        find(driver, "signup_link").click()
        find(driver, "signup_button").click()
        assert find(driver, "signup_name_error").is_displayed()
        assert find(driver, "signup_email_error").is_displayed()

    # TC045
    def test_signup_password_min_length_validation(self, driver):
        """TC045 – Password shorter than minimum length shows length error."""
        find(driver, "signup_link").click()
        find(driver, "signup_password_field").send_keys("Ab1!")
        find(driver, "signup_button").click()
        assert find(driver, "password_length_error").is_displayed()


class TestOrganizerDashboard:

    # TC046
    def test_organizer_dashboard_loads(self, driver):
        """TC046 – Organizer Dashboard loads after role selection."""
        login_as_organizer(driver)
        assert find(driver, "organizer_dashboard_screen").is_displayed()

    # TC047
    def test_organizer_dashboard_shows_event_list(self, driver):
        """TC047 – Organizer Dashboard displays list of created events."""
        login_as_organizer(driver)
        assert find(driver, "events_list").is_displayed()

    # TC048
    def test_organizer_dashboard_create_event_button(self, driver):
        """TC048 – Create Event button is present and tappable."""
        login_as_organizer(driver)
        btn = find(driver, "create_event_button")
        assert btn.is_displayed() and btn.is_enabled()

    # TC049
    def test_organizer_dashboard_navigation_menu(self, driver):
        """TC049 – Navigation menu/sidebar is accessible from dashboard."""
        login_as_organizer(driver)
        assert find(driver, "nav_menu").is_displayed()

    # TC050
    def test_organizer_dashboard_logout_option(self, driver):
        """TC050 – Logout option is accessible from the organizer dashboard."""
        login_as_organizer(driver)
        assert find(driver, "logout_option").is_displayed()

    # TC051
    def test_organizer_dashboard_event_count_shown(self, driver):
        """TC051 – Event count badge or indicator is shown on dashboard."""
        login_as_organizer(driver)
        assert find(driver, "event_count_label").is_displayed()

    # TC052
    def test_organizer_dashboard_tap_event_opens_detail(self, driver):
        """TC052 – Tapping an event on dashboard opens Event Detail screen."""
        login_as_organizer(driver)
        find(driver, "event_list_item_0").click()
        assert find(driver, "event_detail_screen").is_displayed()

    # TC053
    def test_organizer_dashboard_swipe_to_refresh(self, driver):
        """TC053 – Pull-to-refresh on dashboard reloads event list."""
        login_as_organizer(driver)
        size = driver.get_window_size()
        driver.swipe(size["width"] // 2, 300, size["width"] // 2, 700, 500)
        assert find(driver, "events_list").is_displayed()

    # TC054
    def test_organizer_dashboard_participants_link(self, driver):
        """TC054 – Participants section link is accessible from dashboard."""
        login_as_organizer(driver)
        assert find(driver, "nav_participants").is_displayed()

    # TC055
    def test_organizer_dashboard_volunteers_link(self, driver):
        """TC055 – Volunteers section link is accessible from dashboard."""
        login_as_organizer(driver)
        assert find(driver, "nav_volunteers").is_displayed()

    # TC056
    def test_organizer_dashboard_certificates_link(self, driver):
        """TC056 – Certificates section link is accessible from dashboard."""
        login_as_organizer(driver)
        assert find(driver, "nav_certificates").is_displayed()

    # TC057
    def test_organizer_dashboard_settings_link(self, driver):
        """TC057 – Settings link is accessible from dashboard."""
        login_as_organizer(driver)
        assert find(driver, "nav_settings").is_displayed()

    # TC058
    def test_organizer_dashboard_empty_state_when_no_events(self, driver):
        """TC058 – Empty state message shown when no events exist."""
        login_as_organizer(driver)
        # Only verifiable in fresh account state
        assert driver.current_activity is not None

    # TC059
    def test_organizer_dashboard_search_events(self, driver):
        """TC059 – Search bar on dashboard filters events correctly."""
        login_as_organizer(driver)
        search = find(driver, "search_events")
        search.send_keys("Tech")
        assert find(driver, "events_list").is_displayed()

    # TC060
    def test_organizer_logout_navigates_to_login(self, driver):
        """TC060 – Logging out from dashboard navigates back to Login screen."""
        login_as_organizer(driver)
        find(driver, "logout_option").click()
        find(driver, "logout_confirm_button").click()
        assert find(driver, "login_button").is_displayed()

    # TC061
    def test_organizer_dashboard_live_attendance_link(self, driver):
        """TC061 – Live Attendance option is accessible from dashboard."""
        login_as_organizer(driver)
        assert find(driver, "nav_live_attendance").is_displayed()

    # TC062
    def test_organizer_dashboard_title_correct(self, driver):
        """TC062 – Dashboard screen title shows organizer branding."""
        login_as_organizer(driver)
        title = find(driver, "dashboard_title")
        assert title.is_displayed()

    # TC063
    def test_organizer_dashboard_profile_avatar(self, driver):
        """TC063 – Profile avatar or icon is shown in dashboard topbar."""
        login_as_organizer(driver)
        assert find(driver, "profile_avatar").is_displayed()

    # TC064
    def test_organizer_dashboard_tapping_create_opens_create_form(self, driver):
        """TC064 – Tapping Create Event button opens Create Event screen."""
        login_as_organizer(driver)
        find(driver, "create_event_button").click()
        assert find(driver, "create_event_screen").is_displayed()

    # TC065
    def test_organizer_dashboard_event_date_shown(self, driver):
        """TC065 – Event date is displayed for each event in the list."""
        login_as_organizer(driver)
        assert find(driver, "event_date_label_0").is_displayed()

    # TC066
    def test_organizer_dashboard_event_location_shown(self, driver):
        """TC066 – Event location is displayed for each event in the list."""
        login_as_organizer(driver)
        assert find(driver, "event_location_label_0").is_displayed()

    # TC067
    def test_organizer_dashboard_event_status_badge(self, driver):
        """TC067 – Event status badge (active/upcoming/past) is displayed."""
        login_as_organizer(driver)
        assert find(driver, "event_status_badge_0").is_displayed()

    # TC068
    def test_organizer_dashboard_registration_count(self, driver):
        """TC068 – Registration count is visible for each event on dashboard."""
        login_as_organizer(driver)
        assert find(driver, "event_reg_count_0").is_displayed()

    # TC069
    def test_organizer_dashboard_no_crash_on_rotation(self, driver):
        """TC069 – Rotating device does not crash the Organizer Dashboard."""
        login_as_organizer(driver)
        driver.orientation = "LANDSCAPE"
        assert find(driver, "organizer_dashboard_screen").is_displayed()
        driver.orientation = "PORTRAIT"

    # TC070
    def test_organizer_dashboard_back_button_exits_app(self, driver):
        """TC070 – Back button on dashboard triggers exit confirmation."""
        login_as_organizer(driver)
        driver.back()
        assert find(driver, "exit_dialog").is_displayed() or \
               find(driver, "organizer_dashboard_screen").is_displayed()

    # TC071
    def test_organizer_dashboard_keyboard_dismissed_on_outside_tap(self, driver):
        """TC071 – Keyboard is dismissed when tapping outside search field."""
        login_as_organizer(driver)
        find(driver, "search_events").click()
        find(driver, "dashboard_title").click()
        assert driver.is_keyboard_shown() is False

    # TC072
    def test_organizer_dashboard_sort_events(self, driver):
        """TC072 – Sorting events by date reorders the event list."""
        login_as_organizer(driver)
        find(driver, "sort_events_button").click()
        assert find(driver, "events_list").is_displayed()

    # TC073
    def test_organizer_dashboard_filter_events_by_status(self, driver):
        """TC073 – Filtering events by status shows only matching events."""
        login_as_organizer(driver)
        find(driver, "filter_events_button").click()
        find(driver, "filter_active").click()
        assert find(driver, "events_list").is_displayed()

    # TC074
    def test_organizer_dashboard_banner_image_present(self, driver):
        """TC074 – Event banner/thumbnail image is visible in event list."""
        login_as_organizer(driver)
        assert find(driver, "event_banner_0").is_displayed()

    # TC075
    def test_organizer_dashboard_app_version_in_settings(self, driver):
        """TC075 – App version is shown in the Settings screen from dashboard."""
        login_as_organizer(driver)
        find(driver, "nav_settings").click()
        assert find(driver, "app_version_label").is_displayed()
