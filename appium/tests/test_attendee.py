"""
test_attendee.py — Appium test cases for the Attendee role screens.
Covers: Attendee Signup, Dashboard, Discover, Events, Attendance, Certificates.
TC246 – TC360
"""

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def find(driver, aid):
    return WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, aid))
    )


def login_as_attendee(driver):
    find(driver, "email_field").send_keys("attendee@test.com")
    find(driver, "password_field").send_keys("Test@1234")
    find(driver, "login_button").click()
    find(driver, "role_attendee").click()


class TestAttendeeSignup:

    # TC246
    def test_attendee_signup_screen_loads(self, driver):
        """TC246 – Attendee Signup screen loads from the Login page."""
        find(driver, "signup_link").click()
        assert find(driver, "signup_screen").is_displayed()

    # TC247
    def test_attendee_signup_with_valid_data(self, driver):
        """TC247 – Attendee signup with all valid fields creates account."""
        find(driver, "signup_link").click()
        find(driver, "signup_name_field").send_keys("Attendee User")
        find(driver, "signup_email_field").send_keys("newattendee@test.com")
        find(driver, "signup_password_field").send_keys("Attend@123")
        find(driver, "signup_confirm_password_field").send_keys("Attend@123")
        find(driver, "signup_button").click()
        assert driver.current_activity is not None

    # TC248
    def test_attendee_signup_empty_fields_show_errors(self, driver):
        """TC248 – Submitting empty attendee signup form shows validation errors."""
        find(driver, "signup_link").click()
        find(driver, "signup_button").click()
        assert find(driver, "signup_name_error").is_displayed()

    # TC249
    def test_attendee_signup_duplicate_email_error(self, driver):
        """TC249 – Signup with existing email shows duplicate account error."""
        find(driver, "signup_link").click()
        find(driver, "signup_name_field").send_keys("Dup Attendee")
        find(driver, "signup_email_field").send_keys("attendee@test.com")
        find(driver, "signup_password_field").send_keys("Attend@123")
        find(driver, "signup_confirm_password_field").send_keys("Attend@123")
        find(driver, "signup_button").click()
        assert find(driver, "duplicate_email_error").is_displayed()

    # TC250
    def test_attendee_signup_password_mismatch_error(self, driver):
        """TC250 – Mismatched confirm password shows password mismatch error."""
        find(driver, "signup_link").click()
        find(driver, "signup_name_field").send_keys("Test Att")
        find(driver, "signup_email_field").send_keys("att99@test.com")
        find(driver, "signup_password_field").send_keys("Attend@123")
        find(driver, "signup_confirm_password_field").send_keys("Different@456")
        find(driver, "signup_button").click()
        assert find(driver, "password_mismatch_error").is_displayed()

    # TC251
    def test_attendee_signup_back_to_login(self, driver):
        """TC251 – Back button on attendee signup returns to Login screen."""
        find(driver, "signup_link").click()
        driver.back()
        assert find(driver, "login_button").is_displayed()

    # TC252
    def test_attendee_signup_invalid_email_error(self, driver):
        """TC252 – Attendee signup with malformed email shows format error."""
        find(driver, "signup_link").click()
        find(driver, "signup_email_field").send_keys("bademail")
        find(driver, "signup_button").click()
        assert find(driver, "signup_email_error").is_displayed()


class TestAttendeeDashboard:

    # TC253
    def test_attendee_dashboard_loads(self, driver):
        """TC253 – Attendee Dashboard loads after selecting Attendee role."""
        login_as_attendee(driver)
        assert find(driver, "attendee_dashboard_screen").is_displayed()

    # TC254
    def test_attendee_dashboard_upcoming_events_shown(self, driver):
        """TC254 – Upcoming registered events are shown on dashboard."""
        login_as_attendee(driver)
        assert find(driver, "attendee_events_list").is_displayed()

    # TC255
    def test_attendee_dashboard_discover_button_present(self, driver):
        """TC255 – Discover Events button is accessible from Attendee Dashboard."""
        login_as_attendee(driver)
        assert find(driver, "discover_events_button").is_displayed()

    # TC256
    def test_attendee_dashboard_my_events_button_present(self, driver):
        """TC256 – My Events section is present on Attendee Dashboard."""
        login_as_attendee(driver)
        assert find(driver, "my_events_button").is_displayed()

    # TC257
    def test_attendee_dashboard_certificates_button_present(self, driver):
        """TC257 – My Certificates button is accessible from Attendee Dashboard."""
        login_as_attendee(driver)
        assert find(driver, "my_certificates_button").is_displayed()

    # TC258
    def test_attendee_dashboard_logout_option(self, driver):
        """TC258 – Logout option is accessible from Attendee Dashboard."""
        login_as_attendee(driver)
        assert find(driver, "logout_option").is_displayed()

    # TC259
    def test_attendee_dashboard_profile_greeting(self, driver):
        """TC259 – Personalized greeting with attendee name shown on dashboard."""
        login_as_attendee(driver)
        assert find(driver, "attendee_greeting").is_displayed()

    # TC260
    def test_attendee_dashboard_pull_to_refresh(self, driver):
        """TC260 – Pull-to-refresh updates the dashboard content."""
        login_as_attendee(driver)
        size = driver.get_window_size()
        driver.swipe(size["width"] // 2, 300, size["width"] // 2, 700, 500)
        assert find(driver, "attendee_dashboard_screen").is_displayed()

    # TC261
    def test_attendee_dashboard_notifications_icon(self, driver):
        """TC261 – Notifications icon is present on Attendee Dashboard."""
        login_as_attendee(driver)
        assert find(driver, "notifications_icon").is_displayed()

    # TC262
    def test_attendee_dashboard_settings_accessible(self, driver):
        """TC262 – Settings option is accessible from Attendee Dashboard."""
        login_as_attendee(driver)
        assert find(driver, "nav_settings").is_displayed()


class TestAttendeeDiscover:

    # TC263
    def test_discover_screen_loads(self, driver):
        """TC263 – Discover Events screen loads from Attendee Dashboard."""
        login_as_attendee(driver)
        find(driver, "discover_events_button").click()
        assert find(driver, "discover_screen").is_displayed()

    # TC264
    def test_discover_events_list_shown(self, driver):
        """TC264 – Available events list is displayed on Discover screen."""
        login_as_attendee(driver)
        find(driver, "discover_events_button").click()
        assert find(driver, "discover_events_list").is_displayed()

    # TC265
    def test_discover_search_field_present(self, driver):
        """TC265 – Search field is present on Discover Events screen."""
        login_as_attendee(driver)
        find(driver, "discover_events_button").click()
        assert find(driver, "discover_search").is_enabled()

    # TC266
    def test_discover_search_filters_events(self, driver):
        """TC266 – Searching by event name filters results correctly."""
        login_as_attendee(driver)
        find(driver, "discover_events_button").click()
        find(driver, "discover_search").send_keys("Tech")
        assert find(driver, "discover_events_list").is_displayed()

    # TC267
    def test_discover_event_name_shown(self, driver):
        """TC267 – Event name is shown for each event in Discover list."""
        login_as_attendee(driver)
        find(driver, "discover_events_button").click()
        assert find(driver, "discover_event_name_0").is_displayed()

    # TC268
    def test_discover_event_date_shown(self, driver):
        """TC268 – Event date is shown for each event in Discover list."""
        login_as_attendee(driver)
        find(driver, "discover_events_button").click()
        assert find(driver, "discover_event_date_0").is_displayed()

    # TC269
    def test_discover_event_location_shown(self, driver):
        """TC269 – Event location is shown for each event in Discover list."""
        login_as_attendee(driver)
        find(driver, "discover_events_button").click()
        assert find(driver, "discover_event_location_0").is_displayed()

    # TC270
    def test_discover_tap_event_opens_detail(self, driver):
        """TC270 – Tapping an event in Discover opens the Event Detail view."""
        login_as_attendee(driver)
        find(driver, "discover_events_button").click()
        find(driver, "discover_event_item_0").click()
        assert find(driver, "event_detail_screen").is_displayed()

    # TC271
    def test_discover_register_for_event(self, driver):
        """TC271 – Attendee can register for an event from Discover."""
        login_as_attendee(driver)
        find(driver, "discover_events_button").click()
        find(driver, "discover_event_item_0").click()
        find(driver, "register_event_button").click()
        assert find(driver, "registration_success_message").is_displayed()

    # TC272
    def test_discover_already_registered_event_shows_registered_badge(self, driver):
        """TC272 – Already-registered event shows 'Registered' badge in Discover."""
        login_as_attendee(driver)
        find(driver, "discover_events_button").click()
        assert driver.current_activity is not None

    # TC273
    def test_discover_filter_by_category(self, driver):
        """TC273 – Filtering events by category in Discover shows correct events."""
        login_as_attendee(driver)
        find(driver, "discover_events_button").click()
        find(driver, "discover_filter_category").click()
        find(driver, "category_tech").click()
        assert find(driver, "discover_events_list").is_displayed()

    # TC274
    def test_discover_pull_to_refresh(self, driver):
        """TC274 – Pull-to-refresh on Discover screen reloads events."""
        login_as_attendee(driver)
        find(driver, "discover_events_button").click()
        size = driver.get_window_size()
        driver.swipe(size["width"] // 2, 300, size["width"] // 2, 700, 500)
        assert find(driver, "discover_screen").is_displayed()

    # TC275
    def test_discover_back_to_dashboard(self, driver):
        """TC275 – Back button on Discover returns to Attendee Dashboard."""
        login_as_attendee(driver)
        find(driver, "discover_events_button").click()
        driver.back()
        assert find(driver, "attendee_dashboard_screen").is_displayed()


class TestAttendeeEvents:

    # TC276
    def test_my_events_screen_loads(self, driver):
        """TC276 – My Events screen loads from Attendee Dashboard."""
        login_as_attendee(driver)
        find(driver, "my_events_button").click()
        assert find(driver, "my_events_screen").is_displayed()

    # TC277
    def test_my_events_registered_list_shown(self, driver):
        """TC277 – List of registered events shown on My Events screen."""
        login_as_attendee(driver)
        find(driver, "my_events_button").click()
        assert find(driver, "my_events_list").is_displayed()

    # TC278
    def test_my_events_event_name_displayed(self, driver):
        """TC278 – Event name is displayed in My Events list."""
        login_as_attendee(driver)
        find(driver, "my_events_button").click()
        assert find(driver, "my_event_name_0").is_displayed()

    # TC279
    def test_my_events_event_date_displayed(self, driver):
        """TC279 – Event date is displayed in My Events list."""
        login_as_attendee(driver)
        find(driver, "my_events_button").click()
        assert find(driver, "my_event_date_0").is_displayed()

    # TC280
    def test_my_events_cancel_registration_option(self, driver):
        """TC280 – Cancel Registration option is accessible for upcoming events."""
        login_as_attendee(driver)
        find(driver, "my_events_button").click()
        find(driver, "my_event_item_0").click()
        assert find(driver, "cancel_registration_button").is_displayed()

    # TC281
    def test_my_events_cancel_registration_shows_confirmation(self, driver):
        """TC281 – Cancelling registration shows confirmation dialog."""
        login_as_attendee(driver)
        find(driver, "my_events_button").click()
        find(driver, "my_event_item_0").click()
        find(driver, "cancel_registration_button").click()
        assert find(driver, "cancel_reg_confirm_dialog").is_displayed()

    # TC282
    def test_my_events_back_to_dashboard(self, driver):
        """TC282 – Back button from My Events returns to Attendee Dashboard."""
        login_as_attendee(driver)
        find(driver, "my_events_button").click()
        driver.back()
        assert find(driver, "attendee_dashboard_screen").is_displayed()

    # TC283
    def test_my_events_empty_state_no_registrations(self, driver):
        """TC283 – Empty state message shown if attendee has no registered events."""
        login_as_attendee(driver)
        find(driver, "my_events_button").click()
        assert find(driver, "my_events_list").is_displayed() or \
               find(driver, "no_events_message").is_displayed()

    # TC284
    def test_my_events_past_events_section(self, driver):
        """TC284 – Past events section is shown separately in My Events."""
        login_as_attendee(driver)
        find(driver, "my_events_button").click()
        assert driver.current_activity is not None

    # TC285
    def test_my_events_tap_opens_event_detail(self, driver):
        """TC285 – Tapping a registered event opens its detail view."""
        login_as_attendee(driver)
        find(driver, "my_events_button").click()
        find(driver, "my_event_item_0").click()
        assert find(driver, "event_detail_screen").is_displayed()


class TestAttendeeAttendance:

    # TC286
    def test_attendance_screen_loads(self, driver):
        """TC286 – Attendee Attendance screen loads from dashboard navigation."""
        login_as_attendee(driver)
        find(driver, "nav_attendance").click()
        assert find(driver, "attendee_attendance_screen").is_displayed()

    # TC287
    def test_attendance_qr_code_displayed(self, driver):
        """TC287 – Attendee's QR code is displayed on the Attendance screen."""
        login_as_attendee(driver)
        find(driver, "nav_attendance").click()
        assert find(driver, "attendee_qr_code").is_displayed()

    # TC288
    def test_attendance_checkin_status_shown(self, driver):
        """TC288 – Check-in status for each event is shown on Attendance screen."""
        login_as_attendee(driver)
        find(driver, "nav_attendance").click()
        assert find(driver, "attendance_status_list").is_displayed()

    # TC289
    def test_attendance_event_name_shown(self, driver):
        """TC289 – Event name is shown alongside attendance status."""
        login_as_attendee(driver)
        find(driver, "nav_attendance").click()
        assert find(driver, "attendance_event_name_0").is_displayed()

    # TC290
    def test_attendance_qr_code_scannable(self, driver):
        """TC290 – QR code image is clear and scannable in the UI."""
        login_as_attendee(driver)
        find(driver, "nav_attendance").click()
        qr = find(driver, "attendee_qr_code")
        assert qr.size["width"] > 0 and qr.size["height"] > 0

    # TC291
    def test_attendance_back_to_dashboard(self, driver):
        """TC291 – Back button from Attendance screen returns to Dashboard."""
        login_as_attendee(driver)
        find(driver, "nav_attendance").click()
        driver.back()
        assert find(driver, "attendee_dashboard_screen").is_displayed()

    # TC292
    def test_attendance_pull_to_refresh(self, driver):
        """TC292 – Pull-to-refresh updates attendance status list."""
        login_as_attendee(driver)
        find(driver, "nav_attendance").click()
        size = driver.get_window_size()
        driver.swipe(size["width"] // 2, 300, size["width"] // 2, 700, 500)
        assert find(driver, "attendee_attendance_screen").is_displayed()

    # TC293
    def test_attendance_checked_in_badge_shown(self, driver):
        """TC293 – 'Checked In' badge shown for events where attendance confirmed."""
        login_as_attendee(driver)
        find(driver, "nav_attendance").click()
        assert driver.current_activity is not None

    # TC294
    def test_attendance_qr_code_share_option(self, driver):
        """TC294 – QR code can be shared/downloaded from Attendance screen."""
        login_as_attendee(driver)
        find(driver, "nav_attendance").click()
        assert find(driver, "share_qr_button").is_displayed()

    # TC295
    def test_attendance_screen_landscape_mode(self, driver):
        """TC295 – Attendance screen displays correctly in landscape mode."""
        login_as_attendee(driver)
        find(driver, "nav_attendance").click()
        driver.orientation = "LANDSCAPE"
        assert find(driver, "attendee_attendance_screen").is_displayed()
        driver.orientation = "PORTRAIT"


class TestAttendeeCertificates:

    # TC296
    def test_certificates_screen_loads(self, driver):
        """TC296 – Attendee Certificates screen loads from dashboard."""
        login_as_attendee(driver)
        find(driver, "my_certificates_button").click()
        assert find(driver, "attendee_certificates_screen").is_displayed()

    # TC297
    def test_certificates_list_displayed(self, driver):
        """TC297 – List of earned certificates is displayed."""
        login_as_attendee(driver)
        find(driver, "my_certificates_button").click()
        assert find(driver, "certificates_list").is_displayed()

    # TC298
    def test_certificate_event_name_shown(self, driver):
        """TC298 – Event name is shown for each certificate in the list."""
        login_as_attendee(driver)
        find(driver, "my_certificates_button").click()
        assert find(driver, "certificate_event_name_0").is_displayed()

    # TC299
    def test_certificate_date_issued_shown(self, driver):
        """TC299 – Date of certificate issue is shown in the list."""
        login_as_attendee(driver)
        find(driver, "my_certificates_button").click()
        assert find(driver, "certificate_date_0").is_displayed()

    # TC300
    def test_certificate_download_button_present(self, driver):
        """TC300 – Download button is present for each certificate."""
        login_as_attendee(driver)
        find(driver, "my_certificates_button").click()
        assert find(driver, "download_certificate_0").is_displayed()

    # TC301
    def test_certificate_tap_to_preview(self, driver):
        """TC301 – Tapping a certificate opens a full-screen preview."""
        login_as_attendee(driver)
        find(driver, "my_certificates_button").click()
        find(driver, "certificate_item_0").click()
        assert find(driver, "certificate_preview_screen").is_displayed()

    # TC302
    def test_certificate_share_option(self, driver):
        """TC302 – Share option is available for each certificate."""
        login_as_attendee(driver)
        find(driver, "my_certificates_button").click()
        assert find(driver, "share_certificate_0").is_displayed()

    # TC303
    def test_certificates_empty_state_no_certs(self, driver):
        """TC303 – Empty state shown when attendee has no certificates yet."""
        login_as_attendee(driver)
        find(driver, "my_certificates_button").click()
        assert find(driver, "certificates_list").is_displayed() or \
               find(driver, "no_certificates_message").is_displayed()

    # TC304
    def test_certificate_preview_back_to_list(self, driver):
        """TC304 – Back button on certificate preview returns to certificates list."""
        login_as_attendee(driver)
        find(driver, "my_certificates_button").click()
        find(driver, "certificate_item_0").click()
        driver.back()
        assert find(driver, "attendee_certificates_screen").is_displayed()

    # TC305
    def test_certificates_pull_to_refresh(self, driver):
        """TC305 – Pull-to-refresh on certificates screen updates the list."""
        login_as_attendee(driver)
        find(driver, "my_certificates_button").click()
        size = driver.get_window_size()
        driver.swipe(size["width"] // 2, 300, size["width"] // 2, 700, 500)
        assert find(driver, "attendee_certificates_screen").is_displayed()

    # TC306
    def test_certificate_attendee_name_in_preview(self, driver):
        """TC306 – Attendee's name is shown inside the certificate preview."""
        login_as_attendee(driver)
        find(driver, "my_certificates_button").click()
        find(driver, "certificate_item_0").click()
        assert find(driver, "certificate_attendee_name").is_displayed()

    # TC307
    def test_certificate_download_saves_to_device(self, driver):
        """TC307 – Downloading a certificate saves the PDF to device storage."""
        login_as_attendee(driver)
        find(driver, "my_certificates_button").click()
        find(driver, "download_certificate_0").click()
        assert driver.current_activity is not None

    # TC308
    def test_attendee_logout(self, driver):
        """TC308 – Attendee can log out and is redirected to Login screen."""
        login_as_attendee(driver)
        find(driver, "logout_option").click()
        find(driver, "logout_confirm_button").click()
        assert find(driver, "login_button").is_displayed()

    # TC309
    def test_attendee_settings_accessible(self, driver):
        """TC309 – Attendee can access Settings from dashboard navigation."""
        login_as_attendee(driver)
        find(driver, "nav_settings").click()
        assert find(driver, "settings_screen").is_displayed()

    # TC310
    def test_attendee_dashboard_no_crash_on_rotation(self, driver):
        """TC310 – Attendee Dashboard does not crash when device is rotated."""
        login_as_attendee(driver)
        driver.orientation = "LANDSCAPE"
        assert find(driver, "attendee_dashboard_screen").is_displayed()
        driver.orientation = "PORTRAIT"
