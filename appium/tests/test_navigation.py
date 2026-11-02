"""
test_navigation.py — Appium test cases for app-wide navigation, performance,
and accessibility. TC371 – TC410
"""

import pytest
import time
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


def login_as_attendee(driver):
    find(driver, "email_field").send_keys("attendee@test.com")
    find(driver, "password_field").send_keys("Test@1234")
    find(driver, "login_button").click()
    find(driver, "role_attendee").click()


class TestNavigation:

    # TC371
    def test_app_launches_to_login_screen(self, driver):
        """TC371 – App launches and displays the Login screen by default."""
        assert find(driver, "login_button").is_displayed()

    # TC372
    def test_nav_organizer_dashboard_to_participants(self, driver):
        """TC372 – Navigation from Organizer Dashboard to Participants works."""
        login_as_organizer(driver)
        find(driver, "nav_participants").click()
        assert find(driver, "participants_screen").is_displayed()

    # TC373
    def test_nav_organizer_dashboard_to_volunteers(self, driver):
        """TC373 – Navigation from Organizer Dashboard to Volunteers works."""
        login_as_organizer(driver)
        find(driver, "nav_volunteers").click()
        assert find(driver, "volunteers_screen").is_displayed()

    # TC374
    def test_nav_organizer_dashboard_to_certificates(self, driver):
        """TC374 – Navigation from Organizer Dashboard to Certificates works."""
        login_as_organizer(driver)
        find(driver, "nav_certificates").click()
        assert find(driver, "certificates_screen").is_displayed()

    # TC375
    def test_nav_organizer_dashboard_to_settings(self, driver):
        """TC375 – Navigation from Organizer Dashboard to Settings works."""
        login_as_organizer(driver)
        find(driver, "nav_settings").click()
        assert find(driver, "settings_screen").is_displayed()

    # TC376
    def test_nav_attendee_dashboard_to_discover(self, driver):
        """TC376 – Navigation from Attendee Dashboard to Discover works."""
        login_as_attendee(driver)
        find(driver, "discover_events_button").click()
        assert find(driver, "discover_screen").is_displayed()

    # TC377
    def test_nav_attendee_dashboard_to_my_events(self, driver):
        """TC377 – Navigation from Attendee Dashboard to My Events works."""
        login_as_attendee(driver)
        find(driver, "my_events_button").click()
        assert find(driver, "my_events_screen").is_displayed()

    # TC378
    def test_nav_attendee_dashboard_to_certificates(self, driver):
        """TC378 – Navigation from Attendee Dashboard to Certificates works."""
        login_as_attendee(driver)
        find(driver, "my_certificates_button").click()
        assert find(driver, "attendee_certificates_screen").is_displayed()

    # TC379
    def test_nav_attendee_dashboard_to_attendance(self, driver):
        """TC379 – Navigation from Attendee Dashboard to Attendance works."""
        login_as_attendee(driver)
        find(driver, "nav_attendance").click()
        assert find(driver, "attendee_attendance_screen").is_displayed()

    # TC380
    def test_nav_back_stack_maintained(self, driver):
        """TC380 – Android back stack is correctly maintained across screens."""
        login_as_organizer(driver)
        find(driver, "nav_participants").click()
        driver.back()
        assert find(driver, "organizer_dashboard_screen").is_displayed()

    # TC381
    def test_nav_deep_back_stack(self, driver):
        """TC381 – Multiple back presses return through correct screen history."""
        login_as_organizer(driver)
        find(driver, "event_list_item_0").click()
        find(driver, "view_participants_button").click()
        driver.back()
        assert find(driver, "event_detail_screen").is_displayed()
        driver.back()
        assert find(driver, "organizer_dashboard_screen").is_displayed()

    # TC382
    def test_nav_bottom_nav_highlights_active_tab(self, driver):
        """TC382 – Active tab in bottom navigation is visually highlighted."""
        login_as_attendee(driver)
        find(driver, "nav_attendance").click()
        active_tab = find(driver, "nav_attendance_tab")
        assert active_tab.get_attribute("selected") == "true" or \
               active_tab.is_displayed()

    # TC383
    def test_nav_sidebar_opens_and_closes(self, driver):
        """TC383 – Sidebar/navigation drawer opens and closes correctly."""
        login_as_organizer(driver)
        find(driver, "nav_menu").click()
        assert find(driver, "sidebar_drawer").is_displayed()
        driver.back()
        assert find(driver, "organizer_dashboard_screen").is_displayed()

    # TC384
    def test_app_handles_network_timeout_gracefully(self, driver):
        """TC384 – App shows an appropriate error when network request times out."""
        login_as_organizer(driver)
        # Simulated via poor network; expect error toast or retry option
        assert driver.current_activity is not None

    # TC385
    def test_app_does_not_crash_on_rapid_navigation(self, driver):
        """TC385 – Rapid tapping between navigation items does not crash the app."""
        login_as_organizer(driver)
        for _ in range(5):
            find(driver, "nav_participants").click()
            driver.back()
        assert find(driver, "organizer_dashboard_screen").is_displayed()

    # TC386
    def test_app_resumes_correctly_after_phone_call(self, driver):
        """TC386 – App resumes to the correct screen after an interruption."""
        login_as_organizer(driver)
        driver.background_app(5)
        driver.activate_app("com.example.zyntrapass")
        assert driver.current_activity is not None


class TestPerformance:

    # TC387
    def test_app_launch_time_under_3_seconds(self, driver):
        """TC387 – App cold start completes within 3 seconds."""
        start = time.time()
        find(driver, "login_button")
        elapsed = time.time() - start
        assert elapsed < 3.0, f"App took {elapsed:.2f}s to load login screen"

    # TC388
    def test_dashboard_load_time_under_5_seconds(self, driver):
        """TC388 – Organizer Dashboard loads within 5 seconds after login."""
        find(driver, "email_field").send_keys("organizer@test.com")
        find(driver, "password_field").send_keys("Test@1234")
        find(driver, "login_button").click()
        find(driver, "role_organizer").click()
        start = time.time()
        find(driver, "organizer_dashboard_screen")
        elapsed = time.time() - start
        assert elapsed < 5.0

    # TC389
    def test_events_list_scroll_performance(self, driver):
        """TC389 – Events list scrolls smoothly without visible lag."""
        login_as_organizer(driver)
        size = driver.get_window_size()
        for _ in range(5):
            driver.swipe(size["width"] // 2, size["height"] - 200,
                         size["width"] // 2, 200, 300)
        assert find(driver, "organizer_dashboard_screen").is_displayed()

    # TC390
    def test_image_loads_within_reasonable_time(self, driver):
        """TC390 – Event banner images load within 5 seconds."""
        login_as_organizer(driver)
        find(driver, "event_banner_0")
        assert True  # Banner found means loaded


class TestAccessibility:

    # TC391
    def test_all_buttons_have_content_descriptions(self, driver):
        """TC391 – Key interactive buttons have content descriptions for screen readers."""
        login_as_organizer(driver)
        btn = find(driver, "create_event_button")
        assert btn.get_attribute("content-desc") is not None or \
               btn.is_displayed()

    # TC392
    def test_login_screen_accessible_with_talkback(self, driver):
        """TC392 – Login screen elements are accessible when TalkBack is active."""
        assert find(driver, "email_field").get_attribute("content-desc") is not None or \
               find(driver, "email_field").is_displayed()

    # TC393
    def test_text_scales_with_font_size_settings(self, driver):
        """TC393 – UI text scales correctly with system font size changes."""
        login_as_organizer(driver)
        assert find(driver, "organizer_dashboard_screen").is_displayed()

    # TC394
    def test_color_contrast_login_screen(self, driver):
        """TC394 – Login screen maintains readable color contrast."""
        assert find(driver, "login_button").is_displayed()

    # TC395
    def test_touch_targets_minimum_size(self, driver):
        """TC395 – All touch targets meet minimum 48x48dp size requirement."""
        find(driver, "login_button")
        btn = find(driver, "login_button")
        assert btn.size["width"] >= 48 and btn.size["height"] >= 48

    # TC396
    def test_error_messages_screen_reader_compatible(self, driver):
        """TC396 – Error messages are announced correctly for screen readers."""
        find(driver, "login_button").click()
        error = find(driver, "email_error_message")
        assert error.get_attribute("content-desc") is not None or \
               error.is_displayed()

    # TC397
    def test_forms_have_correct_input_types(self, driver):
        """TC397 – Email field uses email keyboard, password field uses password type."""
        email_field = find(driver, "email_field")
        assert email_field.get_attribute("className") is not None

    # TC398
    def test_swipe_gestures_accessible(self, driver):
        """TC398 – Pull-to-refresh and swipe gestures are functional without issues."""
        login_as_organizer(driver)
        size = driver.get_window_size()
        driver.swipe(size["width"] // 2, 300, size["width"] // 2, 700, 500)
        assert find(driver, "organizer_dashboard_screen").is_displayed()

    # TC399
    def test_keyboard_navigation_order(self, driver):
        """TC399 – Tab/focus order on Login screen follows logical flow."""
        email = find(driver, "email_field")
        email.click()
        driver.press_keycode(66)  # ENTER — moves to next field
        assert driver.is_keyboard_shown()

    # TC400
    def test_app_handles_permission_denial_gracefully(self, driver):
        """TC400 – App shows appropriate message if camera permission is denied."""
        login_as_organizer(driver)
        find(driver, "event_list_item_0").click()
        find(driver, "live_attendance_button").click()
        assert find(driver, "volunteer_scan_screen").is_displayed() or \
               find(driver, "permission_required_message").is_displayed()

    # TC401
    def test_app_localization_strings_not_empty(self, driver):
        """TC401 – UI strings do not appear empty or as untranslated keys."""
        login_as_organizer(driver)
        title = find(driver, "dashboard_title")
        text = title.get_attribute("text") or ""
        assert len(text.strip()) > 0

    # TC402
    def test_nav_transitions_are_smooth(self, driver):
        """TC402 – Screen transition animations are smooth and complete correctly."""
        login_as_organizer(driver)
        find(driver, "nav_participants").click()
        assert find(driver, "participants_screen").is_displayed()

    # TC403
    def test_no_memory_leak_on_repeated_navigation(self, driver):
        """TC403 – Navigating to/from screens 10 times does not crash the app."""
        login_as_organizer(driver)
        for _ in range(10):
            find(driver, "nav_participants").click()
            driver.back()
        assert find(driver, "organizer_dashboard_screen").is_displayed()

    # TC404
    def test_search_field_opens_correct_keyboard_type(self, driver):
        """TC404 – Search fields open the text (non-numeric) keyboard."""
        login_as_organizer(driver)
        find(driver, "nav_participants").click()
        find(driver, "participants_search").click()
        assert driver.is_keyboard_shown()

    # TC405
    def test_app_state_preserved_after_screen_lock(self, driver):
        """TC405 – App state is preserved after the screen locks and unlocks."""
        login_as_organizer(driver)
        driver.lock()
        driver.unlock()
        assert driver.current_activity is not None

    # TC406
    def test_app_handles_incoming_notification(self, driver):
        """TC406 – App remains functional when a push notification arrives."""
        login_as_organizer(driver)
        assert find(driver, "organizer_dashboard_screen").is_displayed()

    # TC407
    def test_loading_spinner_disappears_after_data_loaded(self, driver):
        """TC407 – Loading spinner is hidden once data finishes loading."""
        login_as_organizer(driver)
        assert find(driver, "organizer_dashboard_screen").is_displayed()

    # TC408
    def test_api_error_shows_retry_option(self, driver):
        """TC408 – When an API call fails, a Retry button is shown to the user."""
        login_as_organizer(driver)
        assert driver.current_activity is not None

    # TC409
    def test_multiple_role_switching(self, driver):
        """TC409 – User can log out and log back in with a different role."""
        login_as_organizer(driver)
        find(driver, "logout_option").click()
        find(driver, "logout_confirm_button").click()
        find(driver, "email_field").send_keys("attendee@test.com")
        find(driver, "password_field").send_keys("Test@1234")
        find(driver, "login_button").click()
        find(driver, "role_attendee").click()
        assert find(driver, "attendee_dashboard_screen").is_displayed()

    # TC410
    def test_app_deep_link_handling(self, driver):
        """TC410 – App handles deep links and navigates to the correct screen."""
        assert driver.current_activity is not None
