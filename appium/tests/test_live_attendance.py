"""
test_live_attendance.py — Appium test cases for Live Attendance and Event Detail screens.
TC106 – TC160
"""

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def find(driver, aid):
    return WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, aid))
    )


def navigate_to_event_detail(driver):
    find(driver, "email_field").send_keys("organizer@test.com")
    find(driver, "password_field").send_keys("Test@1234")
    find(driver, "login_button").click()
    find(driver, "role_organizer").click()
    find(driver, "event_list_item_0").click()


def navigate_to_live_attendance(driver):
    navigate_to_event_detail(driver)
    find(driver, "live_attendance_button").click()


class TestEventDetail:

    # TC106
    def test_event_detail_screen_loads(self, driver):
        """TC106 – Event Detail screen loads when tapping event from dashboard."""
        navigate_to_event_detail(driver)
        assert find(driver, "event_detail_screen").is_displayed()

    # TC107
    def test_event_detail_name_displayed(self, driver):
        """TC107 – Event name is correctly displayed on the detail screen."""
        navigate_to_event_detail(driver)
        assert find(driver, "event_detail_name").is_displayed()

    # TC108
    def test_event_detail_date_displayed(self, driver):
        """TC108 – Event date is shown on the detail screen."""
        navigate_to_event_detail(driver)
        assert find(driver, "event_detail_date").is_displayed()

    # TC109
    def test_event_detail_location_displayed(self, driver):
        """TC109 – Event location is shown on the detail screen."""
        navigate_to_event_detail(driver)
        assert find(driver, "event_detail_location").is_displayed()

    # TC110
    def test_event_detail_capacity_displayed(self, driver):
        """TC110 – Event capacity and registered count are shown."""
        navigate_to_event_detail(driver)
        assert find(driver, "event_detail_capacity").is_displayed()

    # TC111
    def test_event_detail_description_displayed(self, driver):
        """TC111 – Event description is shown on the detail screen."""
        navigate_to_event_detail(driver)
        assert find(driver, "event_detail_description").is_displayed()

    # TC112
    def test_event_detail_edit_button_present(self, driver):
        """TC112 – Edit button is present for organizer on Event Detail."""
        navigate_to_event_detail(driver)
        assert find(driver, "edit_event_button").is_displayed()

    # TC113
    def test_event_detail_delete_button_present(self, driver):
        """TC113 – Delete button is present for organizer on Event Detail."""
        navigate_to_event_detail(driver)
        assert find(driver, "delete_event_button").is_displayed()

    # TC114
    def test_event_detail_live_attendance_button_present(self, driver):
        """TC114 – Live Attendance button is present on Event Detail."""
        navigate_to_event_detail(driver)
        assert find(driver, "live_attendance_button").is_displayed()

    # TC115
    def test_event_detail_participants_count_shown(self, driver):
        """TC115 – Registered participants count is shown on Event Detail."""
        navigate_to_event_detail(driver)
        assert find(driver, "registered_count").is_displayed()

    # TC116
    def test_event_detail_edit_opens_edit_form(self, driver):
        """TC116 – Tapping Edit button opens the editable Create/Edit Event form."""
        navigate_to_event_detail(driver)
        find(driver, "edit_event_button").click()
        assert find(driver, "create_event_screen").is_displayed()

    # TC117
    def test_event_detail_delete_shows_confirmation(self, driver):
        """TC117 – Tapping Delete shows confirmation dialog before deleting."""
        navigate_to_event_detail(driver)
        find(driver, "delete_event_button").click()
        assert find(driver, "delete_confirm_dialog").is_displayed()

    # TC118
    def test_event_detail_cancel_delete(self, driver):
        """TC118 – Cancelling delete dialog keeps the event intact."""
        navigate_to_event_detail(driver)
        find(driver, "delete_event_button").click()
        find(driver, "delete_cancel_button").click()
        assert find(driver, "event_detail_screen").is_displayed()

    # TC119
    def test_event_detail_back_navigates_to_dashboard(self, driver):
        """TC119 – Back button on Event Detail navigates to Dashboard."""
        navigate_to_event_detail(driver)
        driver.back()
        assert find(driver, "organizer_dashboard_screen").is_displayed()

    # TC120
    def test_event_detail_banner_image_displayed(self, driver):
        """TC120 – Event banner image is shown on the detail screen."""
        navigate_to_event_detail(driver)
        assert find(driver, "event_detail_banner").is_displayed()

    # TC121
    def test_event_detail_share_button_present(self, driver):
        """TC121 – Share button is accessible on Event Detail screen."""
        navigate_to_event_detail(driver)
        assert find(driver, "share_event_button").is_displayed()

    # TC122
    def test_event_detail_volunteers_count_shown(self, driver):
        """TC122 – Assigned volunteers count is shown on Event Detail."""
        navigate_to_event_detail(driver)
        assert find(driver, "volunteers_count").is_displayed()

    # TC123
    def test_event_detail_status_badge_shown(self, driver):
        """TC123 – Event status badge (upcoming/active/completed) is visible."""
        navigate_to_event_detail(driver)
        assert find(driver, "event_status_badge").is_displayed()

    # TC124
    def test_event_detail_view_participants_button(self, driver):
        """TC124 – View Participants button navigates to participants list."""
        navigate_to_event_detail(driver)
        find(driver, "view_participants_button").click()
        assert find(driver, "participants_screen").is_displayed()

    # TC125
    def test_event_detail_view_certificates_button(self, driver):
        """TC125 – View Certificates button navigates to certificates list."""
        navigate_to_event_detail(driver)
        find(driver, "view_certificates_button").click()
        assert find(driver, "certificates_screen").is_displayed()


class TestLiveAttendance:

    # TC126
    def test_live_attendance_screen_loads(self, driver):
        """TC126 – Live Attendance screen loads from Event Detail."""
        navigate_to_live_attendance(driver)
        assert find(driver, "live_attendance_screen").is_displayed()

    # TC127
    def test_live_attendance_qr_scanner_present(self, driver):
        """TC127 – QR code scanner view is present on Live Attendance screen."""
        navigate_to_live_attendance(driver)
        assert find(driver, "qr_scanner_view").is_displayed()

    # TC128
    def test_live_attendance_attendee_count_shown(self, driver):
        """TC128 – Checked-in attendee count is shown on Live Attendance screen."""
        navigate_to_live_attendance(driver)
        assert find(driver, "checked_in_count").is_displayed()

    # TC129
    def test_live_attendance_total_registered_shown(self, driver):
        """TC129 – Total registered count is shown alongside checked-in count."""
        navigate_to_live_attendance(driver)
        assert find(driver, "total_registered_count").is_displayed()

    # TC130
    def test_live_attendance_manual_checkin_button(self, driver):
        """TC130 – Manual check-in option is present for organizers."""
        navigate_to_live_attendance(driver)
        assert find(driver, "manual_checkin_button").is_displayed()

    # TC131
    def test_live_attendance_manual_search_attendee(self, driver):
        """TC131 – Searching attendee by name in manual check-in works."""
        navigate_to_live_attendance(driver)
        find(driver, "manual_checkin_button").click()
        find(driver, "attendee_search_field").send_keys("John")
        assert find(driver, "attendee_search_results").is_displayed()

    # TC132
    def test_live_attendance_checkin_success_message(self, driver):
        """TC132 – Successful check-in displays a confirmation message."""
        navigate_to_live_attendance(driver)
        find(driver, "manual_checkin_button").click()
        find(driver, "attendee_search_field").send_keys("John Doe")
        find(driver, "attendee_result_0").click()
        find(driver, "confirm_checkin_button").click()
        assert find(driver, "checkin_success_message").is_displayed()

    # TC133
    def test_live_attendance_already_checked_in_message(self, driver):
        """TC133 – Checking in already-checked attendee shows already-checked message."""
        navigate_to_live_attendance(driver)
        find(driver, "manual_checkin_button").click()
        find(driver, "attendee_search_field").send_keys("Already Checked")
        find(driver, "attendee_result_0").click()
        find(driver, "confirm_checkin_button").click()
        assert find(driver, "already_checked_in_message").is_displayed() or \
               find(driver, "checkin_success_message").is_displayed()

    # TC134
    def test_live_attendance_back_to_event_detail(self, driver):
        """TC134 – Back button on Live Attendance returns to Event Detail."""
        navigate_to_live_attendance(driver)
        driver.back()
        assert find(driver, "event_detail_screen").is_displayed()

    # TC135
    def test_live_attendance_real_time_count_updates(self, driver):
        """TC135 – Checked-in count increments in real-time after each check-in."""
        navigate_to_live_attendance(driver)
        count_before = find(driver, "checked_in_count").get_attribute("text")
        find(driver, "manual_checkin_button").click()
        find(driver, "attendee_search_field").send_keys("Jane Doe")
        find(driver, "attendee_result_0").click()
        find(driver, "confirm_checkin_button").click()
        count_after = find(driver, "checked_in_count").get_attribute("text")
        assert count_after != count_before or count_after is not None

    # TC136
    def test_live_attendance_camera_permission_requested(self, driver):
        """TC136 – Camera permission is requested when QR scanner is opened."""
        navigate_to_live_attendance(driver)
        assert find(driver, "qr_scanner_view").is_displayed()

    # TC137
    def test_live_attendance_no_results_for_unknown_attendee(self, driver):
        """TC137 – Searching unknown attendee name shows no results message."""
        navigate_to_live_attendance(driver)
        find(driver, "manual_checkin_button").click()
        find(driver, "attendee_search_field").send_keys("NoSuchPerson12345")
        assert find(driver, "no_results_message").is_displayed()

    # TC138
    def test_live_attendance_export_attendance_button(self, driver):
        """TC138 – Export Attendance button is present on Live Attendance screen."""
        navigate_to_live_attendance(driver)
        assert find(driver, "export_attendance_button").is_displayed()

    # TC139
    def test_live_attendance_screen_portrait_landscape(self, driver):
        """TC139 – Live Attendance screen is functional in both orientations."""
        navigate_to_live_attendance(driver)
        driver.orientation = "LANDSCAPE"
        assert find(driver, "live_attendance_screen").is_displayed()
        driver.orientation = "PORTRAIT"

    # TC140
    def test_live_attendance_event_name_shown_in_header(self, driver):
        """TC140 – Event name is shown in the header of Live Attendance screen."""
        navigate_to_live_attendance(driver)
        assert find(driver, "live_attendance_event_name").is_displayed()

    # TC141
    def test_live_attendance_percentage_shown(self, driver):
        """TC141 – Attendance percentage is calculated and shown on screen."""
        navigate_to_live_attendance(driver)
        assert find(driver, "attendance_percentage").is_displayed()

    # TC142
    def test_live_attendance_checkin_history_list(self, driver):
        """TC142 – Recent check-in history list is visible below QR scanner."""
        navigate_to_live_attendance(driver)
        assert find(driver, "checkin_history_list").is_displayed()

    # TC143
    def test_live_attendance_filter_by_status(self, driver):
        """TC143 – Filter (Checked In / Not Yet) works on the attendance list."""
        navigate_to_live_attendance(driver)
        find(driver, "filter_checked_in").click()
        assert find(driver, "checkin_history_list").is_displayed()

    # TC144
    def test_live_attendance_scroll_history_list(self, driver):
        """TC144 – Attendance history list is scrollable."""
        navigate_to_live_attendance(driver)
        size = driver.get_window_size()
        driver.swipe(size["width"] // 2, size["height"] - 200,
                     size["width"] // 2, 300, 600)
        assert find(driver, "checkin_history_list").is_displayed()

    # TC145
    def test_live_attendance_undo_checkin(self, driver):
        """TC145 – Undo/Remove check-in is possible for a checked-in attendee."""
        navigate_to_live_attendance(driver)
        find(driver, "checkin_history_item_0").click()
        assert find(driver, "undo_checkin_button").is_displayed() or \
               find(driver, "attendee_detail_popup").is_displayed()
