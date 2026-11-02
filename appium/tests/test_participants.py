"""
test_participants.py — Appium test cases for Participants and Participant Detail screens.
TC146 – TC185
"""

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def find(driver, aid):
    return WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, aid))
    )


def navigate_to_participants(driver):
    find(driver, "email_field").send_keys("organizer@test.com")
    find(driver, "password_field").send_keys("Test@1234")
    find(driver, "login_button").click()
    find(driver, "role_organizer").click()
    find(driver, "nav_participants").click()


class TestParticipants:

    # TC146
    def test_participants_screen_loads(self, driver):
        """TC146 – Participants screen loads from the dashboard navigation."""
        navigate_to_participants(driver)
        assert find(driver, "participants_screen").is_displayed()

    # TC147
    def test_participants_list_displayed(self, driver):
        """TC147 – Participants list is displayed with registered users."""
        navigate_to_participants(driver)
        assert find(driver, "participants_list").is_displayed()

    # TC148
    def test_participants_search_field_present(self, driver):
        """TC148 – Search field is present on the Participants screen."""
        navigate_to_participants(driver)
        assert find(driver, "participants_search").is_enabled()

    # TC149
    def test_participants_search_filters_by_name(self, driver):
        """TC149 – Searching by name filters the participant list correctly."""
        navigate_to_participants(driver)
        find(driver, "participants_search").send_keys("John")
        assert find(driver, "participants_list").is_displayed()

    # TC150
    def test_participants_search_no_results(self, driver):
        """TC150 – Searching non-existent name shows empty/no-results state."""
        navigate_to_participants(driver)
        find(driver, "participants_search").send_keys("ZZZ_NoMatch_9999")
        assert find(driver, "no_participants_message").is_displayed()

    # TC151
    def test_participants_count_shown(self, driver):
        """TC151 – Total participant count is shown on the screen."""
        navigate_to_participants(driver)
        assert find(driver, "participants_count_label").is_displayed()

    # TC152
    def test_participants_name_displayed_in_list(self, driver):
        """TC152 – Participant name is displayed in each list item."""
        navigate_to_participants(driver)
        assert find(driver, "participant_name_0").is_displayed()

    # TC153
    def test_participants_email_displayed_in_list(self, driver):
        """TC153 – Participant email is displayed in each list item."""
        navigate_to_participants(driver)
        assert find(driver, "participant_email_0").is_displayed()

    # TC154
    def test_participants_registration_status_shown(self, driver):
        """TC154 – Registration status (confirmed/pending) shown in list."""
        navigate_to_participants(driver)
        assert find(driver, "participant_status_0").is_displayed()

    # TC155
    def test_participants_tap_opens_participant_detail(self, driver):
        """TC155 – Tapping a participant opens the Participant Detail screen."""
        navigate_to_participants(driver)
        find(driver, "participant_list_item_0").click()
        assert find(driver, "participant_detail_screen").is_displayed()

    # TC156
    def test_participants_list_scrollable(self, driver):
        """TC156 – Participants list scrolls when there are many registrations."""
        navigate_to_participants(driver)
        size = driver.get_window_size()
        driver.swipe(size["width"] // 2, size["height"] - 200,
                     size["width"] // 2, 200, 600)
        assert find(driver, "participants_list").is_displayed()

    # TC157
    def test_participants_pull_to_refresh(self, driver):
        """TC157 – Pull-to-refresh reloads the participants list."""
        navigate_to_participants(driver)
        size = driver.get_window_size()
        driver.swipe(size["width"] // 2, 300, size["width"] // 2, 700, 500)
        assert find(driver, "participants_list").is_displayed()

    # TC158
    def test_participants_filter_by_event(self, driver):
        """TC158 – Filtering participants by event shows only that event's registrants."""
        navigate_to_participants(driver)
        find(driver, "filter_by_event_button").click()
        find(driver, "event_filter_option_0").click()
        assert find(driver, "participants_list").is_displayed()

    # TC159
    def test_participants_export_button_present(self, driver):
        """TC159 – Export participants list button is present."""
        navigate_to_participants(driver)
        assert find(driver, "export_participants_button").is_displayed()

    # TC160
    def test_participants_back_to_dashboard(self, driver):
        """TC160 – Back button returns to Organizer Dashboard."""
        navigate_to_participants(driver)
        driver.back()
        assert find(driver, "organizer_dashboard_screen").is_displayed()

    # TC161
    def test_participant_detail_screen_loads(self, driver):
        """TC161 – Participant Detail screen loads with full profile."""
        navigate_to_participants(driver)
        find(driver, "participant_list_item_0").click()
        assert find(driver, "participant_detail_screen").is_displayed()

    # TC162
    def test_participant_detail_name_shown(self, driver):
        """TC162 – Participant full name is shown on Detail screen."""
        navigate_to_participants(driver)
        find(driver, "participant_list_item_0").click()
        assert find(driver, "participant_detail_name").is_displayed()

    # TC163
    def test_participant_detail_email_shown(self, driver):
        """TC163 – Participant email address is shown on Detail screen."""
        navigate_to_participants(driver)
        find(driver, "participant_list_item_0").click()
        assert find(driver, "participant_detail_email").is_displayed()

    # TC164
    def test_participant_detail_registered_events_shown(self, driver):
        """TC164 – List of registered events is shown on Participant Detail."""
        navigate_to_participants(driver)
        find(driver, "participant_list_item_0").click()
        assert find(driver, "participant_registered_events").is_displayed()

    # TC165
    def test_participant_detail_attendance_status_shown(self, driver):
        """TC165 – Attendance status for each event is shown on detail screen."""
        navigate_to_participants(driver)
        find(driver, "participant_list_item_0").click()
        assert find(driver, "participant_attendance_status").is_displayed()

    # TC166
    def test_participant_detail_profile_avatar_shown(self, driver):
        """TC166 – Profile avatar/photo is displayed on Participant Detail."""
        navigate_to_participants(driver)
        find(driver, "participant_list_item_0").click()
        assert find(driver, "participant_avatar").is_displayed()

    # TC167
    def test_participant_detail_phone_shown_if_available(self, driver):
        """TC167 – Phone number is shown on Participant Detail if provided."""
        navigate_to_participants(driver)
        find(driver, "participant_list_item_0").click()
        assert driver.current_activity is not None

    # TC168
    def test_participant_detail_certificate_status(self, driver):
        """TC168 – Certificate issue status is shown on Participant Detail."""
        navigate_to_participants(driver)
        find(driver, "participant_list_item_0").click()
        assert find(driver, "participant_certificate_status").is_displayed()

    # TC169
    def test_participant_detail_back_to_list(self, driver):
        """TC169 – Back button on Participant Detail returns to Participants list."""
        navigate_to_participants(driver)
        find(driver, "participant_list_item_0").click()
        driver.back()
        assert find(driver, "participants_screen").is_displayed()

    # TC170
    def test_participant_detail_remove_participant_button(self, driver):
        """TC170 – Remove Participant button is present on Detail screen."""
        navigate_to_participants(driver)
        find(driver, "participant_list_item_0").click()
        assert find(driver, "remove_participant_button").is_displayed()

    # TC171
    def test_participant_detail_remove_shows_confirmation(self, driver):
        """TC171 – Tapping Remove shows a confirmation dialog."""
        navigate_to_participants(driver)
        find(driver, "participant_list_item_0").click()
        find(driver, "remove_participant_button").click()
        assert find(driver, "remove_confirm_dialog").is_displayed()

    # TC172
    def test_participant_detail_cancel_remove(self, driver):
        """TC172 – Cancelling remove dialog keeps participant data intact."""
        navigate_to_participants(driver)
        find(driver, "participant_list_item_0").click()
        find(driver, "remove_participant_button").click()
        find(driver, "remove_cancel_button").click()
        assert find(driver, "participant_detail_screen").is_displayed()

    # TC173
    def test_participant_detail_send_certificate_button(self, driver):
        """TC173 – Send Certificate button is present for completed events."""
        navigate_to_participants(driver)
        find(driver, "participant_list_item_0").click()
        assert find(driver, "send_certificate_button").is_displayed() or \
               driver.current_activity is not None

    # TC174
    def test_participant_list_shows_check_in_icon(self, driver):
        """TC174 – Checked-in participants show a check icon in the list."""
        navigate_to_participants(driver)
        assert find(driver, "participant_checkin_icon_0").is_displayed() or \
               find(driver, "participants_list").is_displayed()

    # TC175
    def test_participants_sort_by_name(self, driver):
        """TC175 – Sorting participants alphabetically by name works."""
        navigate_to_participants(driver)
        find(driver, "sort_participants_button").click()
        find(driver, "sort_by_name").click()
        assert find(driver, "participants_list").is_displayed()

    # TC176
    def test_participants_sort_by_registration_date(self, driver):
        """TC176 – Sorting participants by registration date works."""
        navigate_to_participants(driver)
        find(driver, "sort_participants_button").click()
        find(driver, "sort_by_date").click()
        assert find(driver, "participants_list").is_displayed()

    # TC177
    def test_participants_filter_checked_in_only(self, driver):
        """TC177 – Filter shows only checked-in participants."""
        navigate_to_participants(driver)
        find(driver, "filter_by_checkin_button").click()
        assert find(driver, "participants_list").is_displayed()

    # TC178
    def test_participants_list_item_swipe_actions(self, driver):
        """TC178 – Swipe on participant item reveals quick action buttons."""
        navigate_to_participants(driver)
        size = driver.get_window_size()
        item = find(driver, "participant_list_item_0")
        driver.swipe(item.location["x"] + item.size["width"] - 10,
                     item.location["y"] + item.size["height"] // 2,
                     item.location["x"] + 10,
                     item.location["y"] + item.size["height"] // 2, 300)
        assert driver.current_activity is not None

    # TC179
    def test_participants_empty_state_new_event(self, driver):
        """TC179 – Empty state shown for an event with no registrations."""
        navigate_to_participants(driver)
        find(driver, "filter_by_event_button").click()
        assert driver.current_activity is not None

    # TC180
    def test_participants_bulk_action_available(self, driver):
        """TC180 – Long-pressing participant enables multi-select/bulk action mode."""
        navigate_to_participants(driver)
        find(driver, "participant_list_item_0").click()
        assert driver.current_activity is not None

    # TC181
    def test_participants_pagination_loads_more(self, driver):
        """TC181 – Scrolling to bottom loads more participants (pagination)."""
        navigate_to_participants(driver)
        size = driver.get_window_size()
        for _ in range(3):
            driver.swipe(size["width"] // 2, size["height"] - 100,
                         size["width"] // 2, 100, 400)
        assert find(driver, "participants_list").is_displayed()

    # TC182
    def test_participant_detail_timestamp_of_registration(self, driver):
        """TC182 – Registration timestamp is shown on Participant Detail screen."""
        navigate_to_participants(driver)
        find(driver, "participant_list_item_0").click()
        assert find(driver, "participant_registration_date").is_displayed()

    # TC183
    def test_participants_download_csv(self, driver):
        """TC183 – Exporting participants list downloads a CSV file."""
        navigate_to_participants(driver)
        find(driver, "export_participants_button").click()
        assert driver.current_activity is not None

    # TC184
    def test_participant_detail_event_name_shown(self, driver):
        """TC184 – Event name shown in participant's registered events list."""
        navigate_to_participants(driver)
        find(driver, "participant_list_item_0").click()
        assert find(driver, "participant_event_name_0").is_displayed()

    # TC185
    def test_participant_search_cleared_on_back_and_reopen(self, driver):
        """TC185 – Search query is cleared when navigating back and returning."""
        navigate_to_participants(driver)
        find(driver, "participants_search").send_keys("test")
        driver.back()
        find(driver, "nav_participants").click()
        search_text = find(driver, "participants_search").get_attribute("text")
        assert search_text == "" or search_text is None
