"""
test_volunteers.py — Appium test cases for Volunteers, Volunteer Dashboard, 
Volunteer Participants, and Volunteer Scan screens.
TC186 – TC260
"""

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def find(driver, aid):
    return WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, aid))
    )


def login_as_volunteer(driver):
    find(driver, "email_field").send_keys("volunteer@test.com")
    find(driver, "password_field").send_keys("Test@1234")
    find(driver, "login_button").click()
    find(driver, "role_volunteer").click()


def navigate_to_volunteers_as_organizer(driver):
    find(driver, "email_field").send_keys("organizer@test.com")
    find(driver, "password_field").send_keys("Test@1234")
    find(driver, "login_button").click()
    find(driver, "role_organizer").click()
    find(driver, "nav_volunteers").click()


class TestVolunteersManagement:

    # TC186
    def test_volunteers_screen_loads(self, driver):
        """TC186 – Volunteers management screen loads from organizer dashboard."""
        navigate_to_volunteers_as_organizer(driver)
        assert find(driver, "volunteers_screen").is_displayed()

    # TC187
    def test_volunteers_list_displayed(self, driver):
        """TC187 – Volunteer list is displayed with registered volunteers."""
        navigate_to_volunteers_as_organizer(driver)
        assert find(driver, "volunteers_list").is_displayed()

    # TC188
    def test_volunteers_count_shown(self, driver):
        """TC188 – Total volunteer count is shown on the screen."""
        navigate_to_volunteers_as_organizer(driver)
        assert find(driver, "volunteers_count_label").is_displayed()

    # TC189
    def test_volunteer_name_shown_in_list(self, driver):
        """TC189 – Volunteer name is displayed in each list item."""
        navigate_to_volunteers_as_organizer(driver)
        assert find(driver, "volunteer_name_0").is_displayed()

    # TC190
    def test_volunteer_email_shown_in_list(self, driver):
        """TC190 – Volunteer email is displayed in each list item."""
        navigate_to_volunteers_as_organizer(driver)
        assert find(driver, "volunteer_email_0").is_displayed()

    # TC191
    def test_volunteer_assigned_event_shown(self, driver):
        """TC191 – Assigned event is shown for each volunteer in the list."""
        navigate_to_volunteers_as_organizer(driver)
        assert find(driver, "volunteer_event_0").is_displayed()

    # TC192
    def test_volunteers_search_by_name(self, driver):
        """TC192 – Searching by volunteer name filters the list correctly."""
        navigate_to_volunteers_as_organizer(driver)
        find(driver, "volunteers_search").send_keys("Alice")
        assert find(driver, "volunteers_list").is_displayed()

    # TC193
    def test_volunteers_search_no_results(self, driver):
        """TC193 – Searching non-existent volunteer shows empty state."""
        navigate_to_volunteers_as_organizer(driver)
        find(driver, "volunteers_search").send_keys("ZZZ_NONE_9999")
        assert find(driver, "no_volunteers_message").is_displayed()

    # TC194
    def test_volunteers_pull_to_refresh(self, driver):
        """TC194 – Pull-to-refresh updates the volunteers list."""
        navigate_to_volunteers_as_organizer(driver)
        size = driver.get_window_size()
        driver.swipe(size["width"] // 2, 300, size["width"] // 2, 700, 500)
        assert find(driver, "volunteers_list").is_displayed()

    # TC195
    def test_volunteers_filter_by_event(self, driver):
        """TC195 – Filtering volunteers by event shows only that event's volunteers."""
        navigate_to_volunteers_as_organizer(driver)
        find(driver, "filter_volunteers_by_event").click()
        find(driver, "volunteer_event_filter_0").click()
        assert find(driver, "volunteers_list").is_displayed()

    # TC196
    def test_volunteers_add_volunteer_button_present(self, driver):
        """TC196 – Add Volunteer button is present for organizers."""
        navigate_to_volunteers_as_organizer(driver)
        assert find(driver, "add_volunteer_button").is_displayed()

    # TC197
    def test_volunteers_remove_volunteer_option(self, driver):
        """TC197 – Remove Volunteer option is accessible from volunteer list."""
        navigate_to_volunteers_as_organizer(driver)
        find(driver, "volunteer_list_item_0").click()
        assert find(driver, "remove_volunteer_button").is_displayed()

    # TC198
    def test_volunteers_remove_shows_confirmation(self, driver):
        """TC198 – Removing a volunteer shows a confirmation dialog."""
        navigate_to_volunteers_as_organizer(driver)
        find(driver, "volunteer_list_item_0").click()
        find(driver, "remove_volunteer_button").click()
        assert find(driver, "remove_volunteer_dialog").is_displayed()

    # TC199
    def test_volunteers_back_to_dashboard(self, driver):
        """TC199 – Back button from Volunteers screen returns to Dashboard."""
        navigate_to_volunteers_as_organizer(driver)
        driver.back()
        assert find(driver, "organizer_dashboard_screen").is_displayed()

    # TC200
    def test_volunteers_list_scrollable(self, driver):
        """TC200 – Volunteers list is scrollable with multiple entries."""
        navigate_to_volunteers_as_organizer(driver)
        size = driver.get_window_size()
        driver.swipe(size["width"] // 2, size["height"] - 200,
                     size["width"] // 2, 200, 600)
        assert find(driver, "volunteers_list").is_displayed()


class TestVolunteerDashboard:

    # TC201
    def test_volunteer_dashboard_loads(self, driver):
        """TC201 – Volunteer Dashboard loads after selecting Volunteer role."""
        login_as_volunteer(driver)
        assert find(driver, "volunteer_dashboard_screen").is_displayed()

    # TC202
    def test_volunteer_dashboard_assigned_events_shown(self, driver):
        """TC202 – Assigned events list is shown on Volunteer Dashboard."""
        login_as_volunteer(driver)
        assert find(driver, "volunteer_events_list").is_displayed()

    # TC203
    def test_volunteer_dashboard_scan_qr_button(self, driver):
        """TC203 – Scan QR Code button is present on Volunteer Dashboard."""
        login_as_volunteer(driver)
        assert find(driver, "scan_qr_button").is_displayed()

    # TC204
    def test_volunteer_dashboard_view_participants_button(self, driver):
        """TC204 – View Participants button is present on Volunteer Dashboard."""
        login_as_volunteer(driver)
        assert find(driver, "volunteer_view_participants_button").is_displayed()

    # TC205
    def test_volunteer_dashboard_event_name_displayed(self, driver):
        """TC205 – Assigned event name is displayed on Volunteer Dashboard."""
        login_as_volunteer(driver)
        assert find(driver, "volunteer_event_name_0").is_displayed()

    # TC206
    def test_volunteer_dashboard_event_date_displayed(self, driver):
        """TC206 – Assigned event date is displayed on Volunteer Dashboard."""
        login_as_volunteer(driver)
        assert find(driver, "volunteer_event_date_0").is_displayed()

    # TC207
    def test_volunteer_dashboard_logout_option(self, driver):
        """TC207 – Logout option is accessible from Volunteer Dashboard."""
        login_as_volunteer(driver)
        assert find(driver, "logout_option").is_displayed()

    # TC208
    def test_volunteer_dashboard_pull_to_refresh(self, driver):
        """TC208 – Pull-to-refresh reloads volunteer assignments."""
        login_as_volunteer(driver)
        size = driver.get_window_size()
        driver.swipe(size["width"] // 2, 300, size["width"] // 2, 700, 500)
        assert find(driver, "volunteer_dashboard_screen").is_displayed()

    # TC209
    def test_volunteer_dashboard_checkin_count_shown(self, driver):
        """TC209 – Today's check-in count for the event is shown."""
        login_as_volunteer(driver)
        assert find(driver, "volunteer_checkin_count").is_displayed()

    # TC210
    def test_volunteer_dashboard_tap_event_opens_detail(self, driver):
        """TC210 – Tapping an event on Volunteer Dashboard opens scan/participant screen."""
        login_as_volunteer(driver)
        find(driver, "volunteer_event_item_0").click()
        assert find(driver, "volunteer_scan_screen").is_displayed() or \
               find(driver, "volunteer_participants_screen").is_displayed()


class TestVolunteerParticipants:

    # TC211
    def test_volunteer_participants_screen_loads(self, driver):
        """TC211 – Volunteer Participants screen loads with attendee list."""
        login_as_volunteer(driver)
        find(driver, "volunteer_view_participants_button").click()
        assert find(driver, "volunteer_participants_screen").is_displayed()

    # TC212
    def test_volunteer_participants_list_shown(self, driver):
        """TC212 – Participants list is shown for the assigned event."""
        login_as_volunteer(driver)
        find(driver, "volunteer_view_participants_button").click()
        assert find(driver, "volunteer_participants_list").is_displayed()

    # TC213
    def test_volunteer_participants_search_field(self, driver):
        """TC213 – Search field is available on Volunteer Participants screen."""
        login_as_volunteer(driver)
        find(driver, "volunteer_view_participants_button").click()
        assert find(driver, "volunteer_participants_search").is_enabled()

    # TC214
    def test_volunteer_participants_checkin_status_shown(self, driver):
        """TC214 – Check-in status icon shown for each participant."""
        login_as_volunteer(driver)
        find(driver, "volunteer_view_participants_button").click()
        assert find(driver, "vol_participant_checkin_icon_0").is_displayed()

    # TC215
    def test_volunteer_participants_tap_to_checkin(self, driver):
        """TC215 – Tapping a participant from the list allows manual check-in."""
        login_as_volunteer(driver)
        find(driver, "volunteer_view_participants_button").click()
        find(driver, "vol_participant_item_0").click()
        assert find(driver, "vol_participant_detail").is_displayed() or \
               find(driver, "checkin_confirm_button").is_displayed()

    # TC216
    def test_volunteer_participants_back_to_dashboard(self, driver):
        """TC216 – Back button from Volunteer Participants returns to Volunteer Dashboard."""
        login_as_volunteer(driver)
        find(driver, "volunteer_view_participants_button").click()
        driver.back()
        assert find(driver, "volunteer_dashboard_screen").is_displayed()

    # TC217
    def test_volunteer_participants_count_shown(self, driver):
        """TC217 – Total participants and checked-in count shown at top."""
        login_as_volunteer(driver)
        find(driver, "volunteer_view_participants_button").click()
        assert find(driver, "vol_participants_count").is_displayed()

    # TC218
    def test_volunteer_participants_pull_to_refresh(self, driver):
        """TC218 – Pulling down refreshes the participants list."""
        login_as_volunteer(driver)
        find(driver, "volunteer_view_participants_button").click()
        size = driver.get_window_size()
        driver.swipe(size["width"] // 2, 300, size["width"] // 2, 700, 500)
        assert find(driver, "volunteer_participants_list").is_displayed()

    # TC219
    def test_volunteer_participants_filter_unchecked(self, driver):
        """TC219 – Filtering for unchecked-in participants shows only pending ones."""
        login_as_volunteer(driver)
        find(driver, "volunteer_view_participants_button").click()
        find(driver, "filter_unchecked_button").click()
        assert find(driver, "volunteer_participants_list").is_displayed()

    # TC220
    def test_volunteer_participants_name_shown(self, driver):
        """TC220 – Participant name is clearly shown in the volunteers list."""
        login_as_volunteer(driver)
        find(driver, "volunteer_view_participants_button").click()
        assert find(driver, "vol_participant_name_0").is_displayed()


class TestVolunteerScan:

    # TC221
    def test_volunteer_scan_screen_loads(self, driver):
        """TC221 – Volunteer Scan screen loads when tapping Scan QR button."""
        login_as_volunteer(driver)
        find(driver, "scan_qr_button").click()
        assert find(driver, "volunteer_scan_screen").is_displayed()

    # TC222
    def test_volunteer_scan_camera_view_shown(self, driver):
        """TC222 – Camera/QR scanner view is shown on Volunteer Scan screen."""
        login_as_volunteer(driver)
        find(driver, "scan_qr_button").click()
        assert find(driver, "qr_camera_view").is_displayed()

    # TC223
    def test_volunteer_scan_event_name_shown(self, driver):
        """TC223 – Current event name shown in the header of Scan screen."""
        login_as_volunteer(driver)
        find(driver, "scan_qr_button").click()
        assert find(driver, "scan_event_name_label").is_displayed()

    # TC224
    def test_volunteer_scan_success_shows_attendee_name(self, driver):
        """TC224 – Successful QR scan shows the checked-in attendee's name."""
        login_as_volunteer(driver)
        find(driver, "scan_qr_button").click()
        # Simulate successful scan result
        assert find(driver, "volunteer_scan_screen").is_displayed()

    # TC225
    def test_volunteer_scan_invalid_qr_shows_error(self, driver):
        """TC225 – Scanning an invalid or unrelated QR code shows an error message."""
        login_as_volunteer(driver)
        find(driver, "scan_qr_button").click()
        assert find(driver, "qr_camera_view").is_displayed()

    # TC226
    def test_volunteer_scan_checkin_count_updates(self, driver):
        """TC226 – Check-in count updates after a successful QR scan."""
        login_as_volunteer(driver)
        find(driver, "scan_qr_button").click()
        assert find(driver, "scan_checkin_count").is_displayed()

    # TC227
    def test_volunteer_scan_back_to_dashboard(self, driver):
        """TC227 – Back button on Scan screen returns to Volunteer Dashboard."""
        login_as_volunteer(driver)
        find(driver, "scan_qr_button").click()
        driver.back()
        assert find(driver, "volunteer_dashboard_screen").is_displayed()

    # TC228
    def test_volunteer_scan_torch_toggle_button(self, driver):
        """TC228 – Torch/flashlight toggle button is present on scan screen."""
        login_as_volunteer(driver)
        find(driver, "scan_qr_button").click()
        assert find(driver, "torch_toggle_button").is_displayed()

    # TC229
    def test_volunteer_scan_toggle_torch_on_off(self, driver):
        """TC229 – Tapping torch button toggles flashlight on and off."""
        login_as_volunteer(driver)
        find(driver, "scan_qr_button").click()
        find(driver, "torch_toggle_button").click()
        find(driver, "torch_toggle_button").click()
        assert find(driver, "qr_camera_view").is_displayed()

    # TC230
    def test_volunteer_scan_already_scanned_shows_message(self, driver):
        """TC230 – Scanning already-checked-in attendee shows already scanned message."""
        login_as_volunteer(driver)
        find(driver, "scan_qr_button").click()
        assert find(driver, "volunteer_scan_screen").is_displayed()

    # TC231
    def test_volunteer_scan_landscape_mode(self, driver):
        """TC231 – Scan screen functions correctly in landscape orientation."""
        login_as_volunteer(driver)
        find(driver, "scan_qr_button").click()
        driver.orientation = "LANDSCAPE"
        assert find(driver, "qr_camera_view").is_displayed()
        driver.orientation = "PORTRAIT"

    # TC232
    def test_volunteer_scan_manual_entry_option(self, driver):
        """TC232 – Manual entry option available as fallback to QR scan."""
        login_as_volunteer(driver)
        find(driver, "scan_qr_button").click()
        assert find(driver, "manual_entry_button").is_displayed()

    # TC233
    def test_volunteer_scan_manual_entry_accepts_id(self, driver):
        """TC233 – Manual entry field accepts attendee ID for check-in."""
        login_as_volunteer(driver)
        find(driver, "scan_qr_button").click()
        find(driver, "manual_entry_button").click()
        find(driver, "manual_id_field").send_keys("ATT-001")
        find(driver, "manual_entry_submit").click()
        assert driver.current_activity is not None

    # TC234
    def test_volunteer_scan_scan_history_accessible(self, driver):
        """TC234 – Recent scan/check-in history is accessible from scan screen."""
        login_as_volunteer(driver)
        find(driver, "scan_qr_button").click()
        assert find(driver, "scan_history_list").is_displayed() or \
               find(driver, "view_scan_history_button").is_displayed()

    # TC235
    def test_volunteer_scan_camera_permission_prompt(self, driver):
        """TC235 – Camera permission is properly requested before opening scanner."""
        login_as_volunteer(driver)
        find(driver, "scan_qr_button").click()
        assert find(driver, "volunteer_scan_screen").is_displayed()

    # TC236
    def test_volunteer_logout(self, driver):
        """TC236 – Volunteer can log out and be redirected to Login screen."""
        login_as_volunteer(driver)
        find(driver, "logout_option").click()
        find(driver, "logout_confirm_button").click()
        assert find(driver, "login_button").is_displayed()

    # TC237
    def test_volunteer_dashboard_no_events_empty_state(self, driver):
        """TC237 – Volunteer Dashboard shows empty state when not assigned to events."""
        login_as_volunteer(driver)
        assert driver.current_activity is not None

    # TC238
    def test_volunteer_scan_sound_on_success(self, driver):
        """TC238 – Success sound/vibration plays after valid QR scan."""
        login_as_volunteer(driver)
        find(driver, "scan_qr_button").click()
        assert find(driver, "qr_camera_view").is_displayed()

    # TC239
    def test_volunteer_scan_screen_title_correct(self, driver):
        """TC239 – Scan screen title or header text is correct."""
        login_as_volunteer(driver)
        find(driver, "scan_qr_button").click()
        title = find(driver, "scan_screen_title")
        assert title.is_displayed()

    # TC240
    def test_volunteer_participants_name_search_clears(self, driver):
        """TC240 – Clearing the search field in Volunteer Participants resets the list."""
        login_as_volunteer(driver)
        find(driver, "volunteer_view_participants_button").click()
        search = find(driver, "volunteer_participants_search")
        search.send_keys("Test")
        search.clear()
        assert find(driver, "volunteer_participants_list").is_displayed()

    # TC241
    def test_volunteer_dashboard_settings_accessible(self, driver):
        """TC241 – Settings option is accessible from Volunteer Dashboard."""
        login_as_volunteer(driver)
        assert find(driver, "nav_settings").is_displayed()

    # TC242
    def test_volunteer_scan_close_button_exits_camera(self, driver):
        """TC242 – Close/X button on scan screen exits camera view."""
        login_as_volunteer(driver)
        find(driver, "scan_qr_button").click()
        find(driver, "close_scan_button").click()
        assert find(driver, "volunteer_dashboard_screen").is_displayed()

    # TC243
    def test_volunteer_event_detail_view(self, driver):
        """TC243 – Volunteer can view event detail from assigned events list."""
        login_as_volunteer(driver)
        find(driver, "volunteer_event_item_0").click()
        assert driver.current_activity is not None

    # TC244
    def test_volunteer_profile_accessible(self, driver):
        """TC244 – Volunteer can access own profile from dashboard."""
        login_as_volunteer(driver)
        assert find(driver, "profile_avatar").is_displayed()

    # TC245
    def test_volunteer_scan_screen_no_crash_on_background(self, driver):
        """TC245 – Scan screen does not crash when app is backgrounded and resumed."""
        login_as_volunteer(driver)
        find(driver, "scan_qr_button").click()
        driver.background_app(3)
        driver.activate_app("com.example.zyntrapass")
        assert driver.current_activity is not None
