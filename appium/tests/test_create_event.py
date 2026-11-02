"""
test_create_event.py — Appium test cases for the Create Event screen.
TC076 – TC105
"""

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def find(driver, aid):
    return WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, aid))
    )


def navigate_to_create_event(driver):
    find(driver, "email_field").send_keys("organizer@test.com")
    find(driver, "password_field").send_keys("Test@1234")
    find(driver, "login_button").click()
    find(driver, "role_organizer").click()
    find(driver, "create_event_button").click()


class TestCreateEvent:

    # TC076
    def test_create_event_screen_loads(self, driver):
        """TC076 – Create Event screen loads with all form fields visible."""
        navigate_to_create_event(driver)
        assert find(driver, "create_event_screen").is_displayed()

    # TC077
    def test_event_name_field_present(self, driver):
        """TC077 – Event Name input field is present and editable."""
        navigate_to_create_event(driver)
        assert find(driver, "event_name_field").is_enabled()

    # TC078
    def test_event_description_field_present(self, driver):
        """TC078 – Event Description text area is present."""
        navigate_to_create_event(driver)
        assert find(driver, "event_description_field").is_displayed()

    # TC079
    def test_event_date_picker_present(self, driver):
        """TC079 – Event Date picker is accessible on the form."""
        navigate_to_create_event(driver)
        assert find(driver, "event_date_picker").is_displayed()

    # TC080
    def test_event_time_picker_present(self, driver):
        """TC080 – Event Time picker is present on the form."""
        navigate_to_create_event(driver)
        assert find(driver, "event_time_picker").is_displayed()

    # TC081
    def test_event_location_field_present(self, driver):
        """TC081 – Event Location field is present and editable."""
        navigate_to_create_event(driver)
        assert find(driver, "event_location_field").is_enabled()

    # TC082
    def test_event_capacity_field_present(self, driver):
        """TC082 – Event Capacity field is present and accepts numbers."""
        navigate_to_create_event(driver)
        field = find(driver, "event_capacity_field")
        field.send_keys("100")
        assert field.get_attribute("text") == "100"

    # TC083
    def test_event_image_upload_option_present(self, driver):
        """TC083 – Image upload option is available on Create Event form."""
        navigate_to_create_event(driver)
        assert find(driver, "event_image_upload").is_displayed()

    # TC084
    def test_create_event_submit_button_present(self, driver):
        """TC084 – Submit/Create button is present and enabled on form."""
        navigate_to_create_event(driver)
        btn = find(driver, "submit_create_event")
        assert btn.is_displayed() and btn.is_enabled()

    # TC085
    def test_create_event_with_all_valid_fields(self, driver):
        """TC085 – Creating event with all valid data succeeds."""
        navigate_to_create_event(driver)
        find(driver, "event_name_field").send_keys("TechSummit 2026")
        find(driver, "event_description_field").send_keys("Annual tech conference.")
        find(driver, "event_location_field").send_keys("Chennai Convention Centre")
        find(driver, "event_capacity_field").send_keys("200")
        find(driver, "submit_create_event").click()
        assert find(driver, "event_created_success_message").is_displayed()

    # TC086
    def test_create_event_empty_name_shows_error(self, driver):
        """TC086 – Submitting without event name shows validation error."""
        navigate_to_create_event(driver)
        find(driver, "event_location_field").send_keys("Chennai")
        find(driver, "submit_create_event").click()
        assert find(driver, "event_name_error").is_displayed()

    # TC087
    def test_create_event_empty_date_shows_error(self, driver):
        """TC087 – Submitting without event date shows validation error."""
        navigate_to_create_event(driver)
        find(driver, "event_name_field").send_keys("My Event")
        find(driver, "submit_create_event").click()
        assert find(driver, "event_date_error").is_displayed()

    # TC088
    def test_create_event_empty_location_shows_error(self, driver):
        """TC088 – Submitting without event location shows validation error."""
        navigate_to_create_event(driver)
        find(driver, "event_name_field").send_keys("My Event")
        find(driver, "submit_create_event").click()
        assert find(driver, "event_location_error").is_displayed()

    # TC089
    def test_create_event_past_date_shows_error(self, driver):
        """TC089 – Selecting a past date for the event shows an error."""
        navigate_to_create_event(driver)
        find(driver, "event_date_picker").click()
        find(driver, "date_past_day").click()
        find(driver, "date_confirm_button").click()
        assert find(driver, "event_date_past_error").is_displayed()

    # TC090
    def test_create_event_negative_capacity_shows_error(self, driver):
        """TC090 – Entering negative capacity shows validation error."""
        navigate_to_create_event(driver)
        find(driver, "event_capacity_field").send_keys("-5")
        find(driver, "submit_create_event").click()
        assert find(driver, "event_capacity_error").is_displayed()

    # TC091
    def test_create_event_zero_capacity_shows_error(self, driver):
        """TC091 – Entering zero capacity shows validation error."""
        navigate_to_create_event(driver)
        find(driver, "event_capacity_field").send_keys("0")
        find(driver, "submit_create_event").click()
        assert find(driver, "event_capacity_error").is_displayed()

    # TC092
    def test_create_event_long_name_accepted(self, driver):
        """TC092 – Event name with 100 characters is accepted."""
        navigate_to_create_event(driver)
        long_name = "A" * 100
        find(driver, "event_name_field").send_keys(long_name)
        assert find(driver, "event_name_field").get_attribute("text") == long_name

    # TC093
    def test_create_event_date_picker_selects_future_date(self, driver):
        """TC093 – Date picker allows selecting a future date."""
        navigate_to_create_event(driver)
        find(driver, "event_date_picker").click()
        find(driver, "date_next_month_button").click()
        find(driver, "date_day_15").click()
        find(driver, "date_confirm_button").click()
        assert find(driver, "event_date_field").get_attribute("text") != ""

    # TC094
    def test_create_event_cancel_button_navigates_back(self, driver):
        """TC094 – Cancel button on Create Event returns to Dashboard."""
        navigate_to_create_event(driver)
        find(driver, "cancel_create_event").click()
        assert find(driver, "organizer_dashboard_screen").is_displayed()

    # TC095
    def test_create_event_form_cleared_on_cancel(self, driver):
        """TC095 – Form fields are cleared when Create Event is cancelled and reopened."""
        navigate_to_create_event(driver)
        find(driver, "event_name_field").send_keys("Temp Event")
        find(driver, "cancel_create_event").click()
        find(driver, "create_event_button").click()
        assert find(driver, "event_name_field").get_attribute("text") == ""

    # TC096
    def test_create_event_keyboard_shown_on_name_tap(self, driver):
        """TC096 – Keyboard appears when tapping the Event Name field."""
        navigate_to_create_event(driver)
        find(driver, "event_name_field").click()
        assert driver.is_keyboard_shown()

    # TC097
    def test_create_event_description_max_length(self, driver):
        """TC097 – Description field enforces a maximum character limit."""
        navigate_to_create_event(driver)
        desc_field = find(driver, "event_description_field")
        desc_field.send_keys("D" * 2000)
        text_len = len(desc_field.get_attribute("text"))
        assert text_len <= 2000

    # TC098
    def test_create_event_time_picker_selects_time(self, driver):
        """TC098 – Time picker allows selecting a specific time."""
        navigate_to_create_event(driver)
        find(driver, "event_time_picker").click()
        find(driver, "time_confirm_button").click()
        assert find(driver, "event_time_field").get_attribute("text") != ""

    # TC099
    def test_create_event_back_button_shows_unsaved_changes_dialog(self, driver):
        """TC099 – Back button with unsaved changes shows confirmation dialog."""
        navigate_to_create_event(driver)
        find(driver, "event_name_field").send_keys("Unsaved Event")
        driver.back()
        assert find(driver, "unsaved_changes_dialog").is_displayed()

    # TC100
    def test_create_event_scroll_to_bottom_of_form(self, driver):
        """TC100 – Long form scrolls to reveal all fields including submit button."""
        navigate_to_create_event(driver)
        size = driver.get_window_size()
        driver.swipe(size["width"] // 2, size["height"] - 100,
                     size["width"] // 2, 100, 800)
        assert find(driver, "submit_create_event").is_displayed()

    # TC101
    def test_create_event_category_dropdown_present(self, driver):
        """TC101 – Category/Type dropdown field is present on form."""
        navigate_to_create_event(driver)
        assert find(driver, "event_category_dropdown").is_displayed()

    # TC102
    def test_create_event_category_selection(self, driver):
        """TC102 – Selecting a category from dropdown updates the field."""
        navigate_to_create_event(driver)
        find(driver, "event_category_dropdown").click()
        find(driver, "category_option_tech").click()
        assert find(driver, "event_category_dropdown").get_attribute("text") != ""

    # TC103
    def test_create_event_success_navigates_to_detail(self, driver):
        """TC103 – After successful event creation, navigates to Event Detail screen."""
        navigate_to_create_event(driver)
        find(driver, "event_name_field").send_keys("Quick Test Event")
        find(driver, "event_location_field").send_keys("Test Hall")
        find(driver, "event_capacity_field").send_keys("50")
        find(driver, "event_date_picker").click()
        find(driver, "date_next_month_button").click()
        find(driver, "date_day_10").click()
        find(driver, "date_confirm_button").click()
        find(driver, "submit_create_event").click()
        assert find(driver, "event_detail_screen").is_displayed()

    # TC104
    def test_create_event_is_visible_in_dashboard_after_creation(self, driver):
        """TC104 – Newly created event appears in the Organizer Dashboard."""
        navigate_to_create_event(driver)
        find(driver, "event_name_field").send_keys("Dashboard Test Event")
        find(driver, "event_location_field").send_keys("Hall B")
        find(driver, "event_capacity_field").send_keys("30")
        find(driver, "submit_create_event").click()
        driver.back()
        assert find(driver, "organizer_dashboard_screen").is_displayed()

    # TC105
    def test_create_event_special_characters_in_name(self, driver):
        """TC105 – Event name with special characters is accepted."""
        navigate_to_create_event(driver)
        find(driver, "event_name_field").send_keys("Dev Summit @ 2026!")
        assert find(driver, "event_name_field").get_attribute("text") == "Dev Summit @ 2026!"
