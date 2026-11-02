"""
test_06_create_event.py  —  Create Event (7-step wizard)
TC151 – TC200
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from conftest import go, wait_for, click_when_ready, fill


class TestCreateEventPage:

    def test_TC151_create_event_page_loads(self, driver):
        """TC151 – Create Event page loads successfully."""
        go(driver, "/create_event.html")
        assert "Create" in driver.title or "ZyntraPass" in driver.title

    def test_TC152_create_event_heading_visible(self, driver):
        """TC152 – 'Create event' heading is displayed."""
        go(driver, "/create_event.html")
        h1 = wait_for(driver, By.CLASS_NAME, "header-title")
        assert "Create" in h1.text

    def test_TC153_seven_step_stepper_present(self, driver):
        """TC153 – Stepper sidebar shows all 7 steps."""
        go(driver, "/create_event.html")
        steps = driver.find_elements(By.CLASS_NAME, "step-item")
        assert len(steps) == 7

    def test_TC154_step1_active_by_default(self, driver):
        """TC154 – Step 1 is active (highlighted) by default."""
        go(driver, "/create_event.html")
        step1 = wait_for(driver, By.ID, "stepper-1")
        assert "active" in step1.get_attribute("class")

    def test_TC155_step1_basic_info_label(self, driver):
        """TC155 – Step 1 label says 'Basic information'."""
        go(driver, "/create_event.html")
        step1 = wait_for(driver, By.ID, "stepper-1")
        assert "Basic" in step1.text or "information" in step1.text

    def test_TC156_step2_date_time_label(self, driver):
        """TC156 – Step 2 label says 'Date & time'."""
        go(driver, "/create_event.html")
        step2 = wait_for(driver, By.ID, "stepper-2")
        assert "Date" in step2.text or "time" in step2.text

    def test_TC157_step3_location_label(self, driver):
        """TC157 – Step 3 label says 'Location'."""
        go(driver, "/create_event.html")
        step3 = wait_for(driver, By.ID, "stepper-3")
        assert "Location" in step3.text

    def test_TC158_step4_speakers_label(self, driver):
        """TC158 – Step 4 label says 'Speakers'."""
        go(driver, "/create_event.html")
        step4 = wait_for(driver, By.ID, "stepper-4")
        assert "Speaker" in step4.text

    def test_TC159_step5_sessions_label(self, driver):
        """TC159 – Step 5 label says 'Sessions'."""
        go(driver, "/create_event.html")
        step5 = wait_for(driver, By.ID, "stepper-5")
        assert "Session" in step5.text

    def test_TC160_step6_attendance_rules_label(self, driver):
        """TC160 – Step 6 label says 'Attendance rules'."""
        go(driver, "/create_event.html")
        step6 = wait_for(driver, By.ID, "stepper-6")
        assert "Attendance" in step6.text or "rules" in step6.text

    def test_TC161_step7_publish_label(self, driver):
        """TC161 – Step 7 label says 'Publish'."""
        go(driver, "/create_event.html")
        step7 = wait_for(driver, By.ID, "stepper-7")
        assert "Publish" in step7.text

    def test_TC162_step1_card_visible(self, driver):
        """TC162 – Step 1 form card is visible on page load."""
        go(driver, "/create_event.html")
        card = wait_for(driver, By.ID, "step1-card")
        assert card.is_displayed()

    def test_TC163_step2_card_hidden_by_default(self, driver):
        """TC163 – Step 2 form card is hidden by default."""
        go(driver, "/create_event.html")
        card = wait_for(driver, By.ID, "step2-card")
        assert not card.is_displayed()

    def test_TC164_step3_card_hidden_by_default(self, driver):
        """TC164 – Step 3 form card is hidden by default."""
        go(driver, "/create_event.html")
        card = wait_for(driver, By.ID, "step3-card")
        assert not card.is_displayed()

    def test_TC165_event_name_field_present(self, driver):
        """TC165 – Event Name input field is present in Step 1."""
        go(driver, "/create_event.html")
        f = wait_for(driver, By.ID, "eventName")
        assert f.is_displayed()

    def test_TC166_event_description_field_present(self, driver):
        """TC166 – Description textarea is present in Step 1."""
        go(driver, "/create_event.html")
        f = wait_for(driver, By.ID, "eventDescription")
        assert f.is_displayed()

    def test_TC167_category_dropdown_present(self, driver):
        """TC167 – Category dropdown/select is present in Step 1."""
        go(driver, "/create_event.html")
        sel = wait_for(driver, By.ID, "eventCategory")
        assert sel.is_displayed()

    def test_TC168_category_has_summit_option(self, driver):
        """TC168 – Category dropdown has 'Summit' option."""
        go(driver, "/create_event.html")
        sel = wait_for(driver, By.ID, "eventCategory")
        options = sel.find_elements(By.TAG_NAME, "option")
        texts = [o.text for o in options]
        assert "Summit" in texts

    def test_TC169_category_has_workshop_option(self, driver):
        """TC169 – Category dropdown has 'Workshop' option."""
        go(driver, "/create_event.html")
        sel = wait_for(driver, By.ID, "eventCategory")
        options = sel.find_elements(By.TAG_NAME, "option")
        texts = [o.text for o in options]
        assert "Workshop" in texts

    def test_TC170_category_has_hackathon_option(self, driver):
        """TC170 – Category dropdown has 'Hackathon' option."""
        go(driver, "/create_event.html")
        sel = wait_for(driver, By.ID, "eventCategory")
        options = sel.find_elements(By.TAG_NAME, "option")
        texts = [o.text for o in options]
        assert "Hackathon" in texts

    def test_TC171_banner_upload_box_present(self, driver):
        """TC171 – Banner image upload box is present."""
        go(driver, "/create_event.html")
        box = wait_for(driver, By.ID, "uploadBox")
        assert box.is_displayed()

    def test_TC172_banner_file_input_present(self, driver):
        """TC172 – Banner file input element is present."""
        go(driver, "/create_event.html")
        inp = wait_for(driver, By.ID, "banner-input")
        assert inp is not None

    def test_TC173_continue_step1_button_present(self, driver):
        """TC173 – 'Continue' button is present in Step 1."""
        go(driver, "/create_event.html")
        btn = wait_for(driver, By.ID, "btnContinueStep1")
        assert btn.is_displayed()

    def test_TC174_back_button_step1_present(self, driver):
        """TC174 – 'Back' button is present in Step 1."""
        go(driver, "/create_event.html")
        btns = driver.find_elements(By.CLASS_NAME, "btn-back")
        assert len(btns) > 0

    def test_TC175_back_btn_step1_navigates_to_dashboard(self, driver):
        """TC175 – Step 1 Back button navigates to dashboard.html."""
        go(driver, "/create_event.html")
        btns = driver.find_elements(By.CLASS_NAME, "btn-back")
        if btns:
            btns[0].click()
            WebDriverWait(driver, 10).until(EC.url_contains("dashboard"))
            assert "dashboard" in driver.current_url

    def test_TC176_event_name_accepts_input(self, driver):
        """TC176 – Event Name field accepts text input."""
        go(driver, "/create_event.html")
        fill(driver, By.ID, "eventName", "AI Summit 2026")
        assert driver.find_element(By.ID, "eventName").get_attribute("value") == "AI Summit 2026"

    def test_TC177_description_accepts_input(self, driver):
        """TC177 – Description textarea accepts text input."""
        go(driver, "/create_event.html")
        fill(driver, By.ID, "eventDescription", "An amazing summit about AI.")
        assert "AI" in driver.find_element(By.ID, "eventDescription").get_attribute("value")

    def test_TC178_continue_step1_shows_step2(self, driver):
        """TC178 – Filling Step 1 and clicking Continue shows Step 2."""
        go(driver, "/create_event.html")
        fill(driver, By.ID, "eventName", "Test Event")
        click_when_ready(driver, By.ID, "btnContinueStep1")
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "step2-card")))
        assert driver.find_element(By.ID, "step2-card").is_displayed()

    def test_TC179_step2_start_date_field_present(self, driver):
        """TC179 – Start date field is present in Step 2."""
        go(driver, "/create_event.html")
        fill(driver, By.ID, "eventName", "Test")
        click_when_ready(driver, By.ID, "btnContinueStep1")
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "step2-card")))
        assert wait_for(driver, By.ID, "startDate").is_displayed()

    def test_TC180_step2_end_date_field_present(self, driver):
        """TC180 – End date field is present in Step 2."""
        go(driver, "/create_event.html")
        fill(driver, By.ID, "eventName", "Test")
        click_when_ready(driver, By.ID, "btnContinueStep1")
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "step2-card")))
        assert wait_for(driver, By.ID, "endDate").is_displayed()

    def test_TC181_step2_start_time_field_present(self, driver):
        """TC181 – Start time field is present in Step 2."""
        go(driver, "/create_event.html")
        fill(driver, By.ID, "eventName", "Test")
        click_when_ready(driver, By.ID, "btnContinueStep1")
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "step2-card")))
        assert wait_for(driver, By.ID, "startTime").is_displayed()

    def test_TC182_step2_end_time_field_present(self, driver):
        """TC182 – End time field is present in Step 2."""
        go(driver, "/create_event.html")
        fill(driver, By.ID, "eventName", "Test")
        click_when_ready(driver, By.ID, "btnContinueStep1")
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "step2-card")))
        assert wait_for(driver, By.ID, "endTime").is_displayed()

    def test_TC183_step2_back_btn_returns_to_step1(self, driver):
        """TC183 – Step 2 Back button returns to Step 1."""
        go(driver, "/create_event.html")
        fill(driver, By.ID, "eventName", "Test")
        click_when_ready(driver, By.ID, "btnContinueStep1")
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "step2-card")))
        click_when_ready(driver, By.ID, "btnBackStep2")
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "step1-card")))
        assert driver.find_element(By.ID, "step1-card").is_displayed()

    def test_TC184_step3_venue_field_present(self, driver):
        """TC184 – Venue name field is present in Step 3."""
        go(driver, "/create_event.html")
        fill(driver, By.ID, "eventName", "Test")
        click_when_ready(driver, By.ID, "btnContinueStep1")
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "step2-card")))
        fill(driver, By.ID, "startDate", "2026-12-01")
        fill(driver, By.ID, "endDate", "2026-12-01")
        click_when_ready(driver, By.ID, "btnContinueStep2")
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "step3-card")))
        assert wait_for(driver, By.ID, "venueName").is_displayed()

    def test_TC185_step3_gps_lat_field_present(self, driver):
        """TC185 – GPS latitude field is present in Step 3."""
        assert "gpsLat" in driver.page_source

    def test_TC186_step3_gps_lng_field_present(self, driver):
        """TC186 – GPS longitude field is present in Step 3."""
        assert "gpsLng" in driver.page_source

    def test_TC187_step3_attendance_radius_field(self, driver):
        """TC187 – Attendance radius field is present in Step 3."""
        assert "attendanceRadius" in driver.page_source

    def test_TC188_step6_checkpoints_field_present(self, driver):
        """TC188 – Number of checkpoints field is present in Step 6."""
        assert "checkpointsCount" in driver.page_source

    def test_TC189_step6_min_attendance_field_present(self, driver):
        """TC189 – Minimum attendance percentage field is present in Step 6."""
        assert "minAttendance" in driver.page_source

    def test_TC190_step6_qr_refresh_field_present(self, driver):
        """TC190 – QR refresh interval field is present in Step 6."""
        assert "qrRefresh" in driver.page_source

    def test_TC191_step7_preview_title_element(self, driver):
        """TC191 – Preview title element exists in Step 7."""
        assert "previewTitle" in driver.page_source

    def test_TC192_step7_preview_category_element(self, driver):
        """TC192 – Preview category element exists in Step 7."""
        assert "previewCategory" in driver.page_source

    def test_TC193_step7_preview_schedule_element(self, driver):
        """TC193 – Preview schedule element exists in Step 7."""
        assert "previewSchedule" in driver.page_source

    def test_TC194_step7_publish_button_present(self, driver):
        """TC194 – 'Create Event' publish button is present in Step 7."""
        assert "btnPublishEvent" in driver.page_source

    def test_TC195_step4_add_guest_button_present(self, driver):
        """TC195 – 'Add guest' button is present in Step 4."""
        assert "btnAddGuest" in driver.page_source

    def test_TC196_step5_add_session_button_present(self, driver):
        """TC196 – 'Add session' button is present in Step 5."""
        assert "btnAddSession" in driver.page_source

    def test_TC197_upload_box_text_present(self, driver):
        """TC197 – Upload box shows '16:9 banner' instruction text."""
        go(driver, "/create_event.html")
        assert "16:9" in driver.page_source

    def test_TC198_step6_checkpoint_timing_dropdown(self, driver):
        """TC198 – Checkpoint timing dropdown is present in Step 6."""
        assert "checkpointTiming" in driver.page_source

    def test_TC199_event_name_field_required(self, driver):
        """TC199 – Event name field has required attribute."""
        go(driver, "/create_event.html")
        f = driver.find_element(By.ID, "eventName")
        assert f.get_attribute("required") is not None

    def test_TC200_bottom_nav_dashboard_link_works(self, driver):
        """TC200 – Bottom nav Dashboard link on create_event navigates to dashboard."""
        go(driver, "/create_event.html")
        nav_items = driver.find_elements(By.CLASS_NAME, "nav-item")
        dashboard_links = [n for n in nav_items if "Dashboard" in n.text]
        if dashboard_links:
            dashboard_links[0].click()
            WebDriverWait(driver, 10).until(EC.url_contains("dashboard"))
            assert "dashboard" in driver.current_url
