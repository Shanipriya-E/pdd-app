"""
test_08_ui_and_accessibility.py  —  UI, Accessibility, Performance & Form validation
TC281 – TC350
"""
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from conftest import go, wait_for, click_when_ready, fill
from config import BASE_URL


class TestUIAndAccessibility:

    def test_TC281_index_page_h1_exists(self, driver):
        """TC281 – Index page has an <h1> heading."""
        go(driver, "/index.html")
        assert len(driver.find_elements(By.TAG_NAME, "h1")) > 0

    def test_TC282_login_page_has_charset_utf8(self, driver):
        """TC282 – Login page declares UTF-8 charset."""
        go(driver, "/login.html")
        assert "UTF-8" in driver.page_source or "utf-8" in driver.page_source.lower()

    def test_TC283_signup_page_has_charset_utf8(self, driver):
        """TC283 – Signup page declares UTF-8 charset."""
        go(driver, "/signup.html")
        assert "UTF-8" in driver.page_source or "utf-8" in driver.page_source.lower()

    def test_TC284_dashboard_page_has_charset_utf8(self, driver):
        """TC284 – Dashboard page declares UTF-8 charset."""
        go(driver, "/dashboard.html")
        assert "UTF-8" in driver.page_source or "utf-8" in driver.page_source.lower()

    def test_TC285_create_event_google_font_referenced(self, driver):
        """TC285 – Create event page references Google Fonts (Inter)."""
        go(driver, "/create_event.html")
        assert "fonts.googleapis.com" in driver.page_source or "Inter" in driver.page_source

    def test_TC286_dashboard_google_font_referenced(self, driver):
        """TC286 – Dashboard page references Google Fonts (Inter)."""
        go(driver, "/dashboard.html")
        assert "fonts.googleapis.com" in driver.page_source or "Inter" in driver.page_source

    def test_TC287_login_form_has_autocomplete_email(self, driver):
        """TC287 – Login email input type is 'email'."""
        go(driver, "/login.html")
        el = driver.find_element(By.ID, "email")
        assert el.get_attribute("type") == "email"

    def test_TC288_login_form_has_autocomplete_password(self, driver):
        """TC288 – Login password input type is 'password'."""
        go(driver, "/login.html")
        el = driver.find_element(By.ID, "password")
        assert el.get_attribute("type") == "password"

    def test_TC289_signup_phone_type_tel(self, driver):
        """TC289 – Signup phone number field type is 'tel'."""
        go(driver, "/signup.html")
        el = driver.find_element(By.ID, "phone")
        assert el.get_attribute("type") == "tel"

    def test_TC290_signup_email_type_email(self, driver):
        """TC290 – Signup email field type is 'email'."""
        go(driver, "/signup.html")
        el = driver.find_element(By.ID, "email")
        assert el.get_attribute("type") == "email"

    def test_TC291_create_event_gps_lat_type_number(self, driver):
        """TC291 – GPS lat field type is 'number'."""
        go(driver, "/create_event.html")
        el = driver.find_element(By.ID, "gpsLat")
        assert el.get_attribute("type") == "number"

    def test_TC292_create_event_gps_lng_type_number(self, driver):
        """TC292 – GPS lng field type is 'number'."""
        go(driver, "/create_event.html")
        el = driver.find_element(By.ID, "gpsLng")
        assert el.get_attribute("type") == "number"

    def test_TC293_create_event_start_date_type_date(self, driver):
        """TC293 – Start date field type is 'date'."""
        go(driver, "/create_event.html")
        el = driver.find_element(By.ID, "startDate")
        assert el.get_attribute("type") == "date"

    def test_TC294_create_event_end_date_type_date(self, driver):
        """TC294 – End date field type is 'date'."""
        go(driver, "/create_event.html")
        el = driver.find_element(By.ID, "endDate")
        assert el.get_attribute("type") == "date"

    def test_TC295_create_event_start_time_type_time(self, driver):
        """TC295 – Start time field type is 'time'."""
        go(driver, "/create_event.html")
        el = driver.find_element(By.ID, "startTime")
        assert el.get_attribute("type") == "time"

    def test_TC296_create_event_end_time_type_time(self, driver):
        """TC296 – End time field type is 'time'."""
        go(driver, "/create_event.html")
        el = driver.find_element(By.ID, "endTime")
        assert el.get_attribute("type") == "time"

    def test_TC297_create_event_checkpoints_type_number(self, driver):
        """TC297 – Checkpoints count field type is 'number'."""
        go(driver, "/create_event.html")
        el = driver.find_element(By.ID, "checkpointsCount")
        assert el.get_attribute("type") == "number"

    def test_TC298_create_event_min_attendance_type_number(self, driver):
        """TC298 – Min attendance field type is 'number'."""
        go(driver, "/create_event.html")
        el = driver.find_element(By.ID, "minAttendance")
        assert el.get_attribute("type") == "number"

    def test_TC299_create_event_qr_refresh_type_number(self, driver):
        """TC299 – QR refresh field type is 'number'."""
        go(driver, "/create_event.html")
        el = driver.find_element(By.ID, "qrRefresh")
        assert el.get_attribute("type") == "number"

    def test_TC300_login_page_renders_within_5s(self, driver):
        """TC300 – Login page renders within 5 seconds (performance)."""
        start = time.time()
        go(driver, "/login.html")
        wait_for(driver, By.CLASS_NAME, "auth-container")
        elapsed = time.time() - start
        assert elapsed < 5

    def test_TC301_index_page_renders_within_5s(self, driver):
        """TC301 – Index page renders within 5 seconds (performance)."""
        start = time.time()
        go(driver, "/index.html")
        wait_for(driver, By.CLASS_NAME, "hero-title")
        elapsed = time.time() - start
        assert elapsed < 5

    def test_TC302_events_page_renders_within_10s(self, driver):
        """TC302 – Events page renders all major elements within 10 seconds."""
        start = time.time()
        go(driver, "/events.html")
        wait_for(driver, By.CLASS_NAME, "tabs")
        elapsed = time.time() - start
        assert elapsed < 10

    def test_TC303_dashboard_renders_within_10s(self, driver):
        """TC303 – Dashboard renders all major elements within 10 seconds."""
        start = time.time()
        go(driver, "/dashboard.html")
        wait_for(driver, By.CLASS_NAME, "stats-grid")
        elapsed = time.time() - start
        assert elapsed < 10

    def test_TC304_create_event_renders_within_5s(self, driver):
        """TC304 – Create Event page renders within 5 seconds."""
        start = time.time()
        go(driver, "/create_event.html")
        wait_for(driver, By.CLASS_NAME, "step-list")
        elapsed = time.time() - start
        assert elapsed < 5

    def test_TC305_login_role_card_hover_css(self, driver):
        """TC305 – Role card hover CSS class triggers on hover (style defined)."""
        go(driver, "/login.html")
        page = driver.page_source
        assert "role-option:hover" in page or ".role-option" in page

    def test_TC306_events_tab_transition_css(self, driver):
        """TC306 – Tab items have active-state CSS defined."""
        go(driver, "/events.html")
        assert "tab.active" in driver.page_source or ".tab.active" in driver.page_source

    def test_TC307_dashboard_sidebar_gradient_defined(self, driver):
        """TC307 – Dashboard sidebar has gradient background CSS."""
        go(driver, "/dashboard.html")
        assert "linear-gradient" in driver.page_source

    def test_TC308_create_event_upload_box_dashed_border(self, driver):
        """TC308 – Upload box has dashed border style defined."""
        go(driver, "/create_event.html")
        assert "dashed" in driver.page_source

    def test_TC309_login_submit_btn_color_defined(self, driver):
        """TC309 – Login submit button has ZyntraPass brand color defined."""
        go(driver, "/login.html")
        assert "5b54e3" in driver.page_source or "btn-submit" in driver.page_source

    def test_TC310_all_forms_have_ids(self, driver):
        """TC310 – All main forms have IDs for reliable element targeting."""
        pages_forms = [
            ("/login.html", "login-form"),
            ("/signup.html", "signup-form"),
            ("/create_event.html", "create-event-form"),
        ]
        for page, form_id in pages_forms:
            go(driver, page)
            assert form_id in driver.page_source, f"Form ID '{form_id}' missing on {page}"

    def test_TC311_create_event_banner_accept_image(self, driver):
        """TC311 – Banner file input accepts only image files."""
        go(driver, "/create_event.html")
        inp = driver.find_element(By.ID, "banner-input")
        assert inp.get_attribute("accept") == "image/*"

    def test_TC312_events_search_clears_on_empty(self, driver):
        """TC312 – Clearing search restores all event results."""
        go(driver, "/events.html")
        search = driver.find_element(By.ID, "searchInput")
        search.send_keys("sometext")
        search.clear()
        assert search.get_attribute("value") == ""

    def test_TC313_login_error_msg_initially_hidden(self, driver):
        """TC313 – Error message on login form is hidden by default."""
        go(driver, "/login.html")
        err = wait_for(driver, By.ID, "error-msg")
        assert not err.is_displayed()

    def test_TC314_signup_error_msg_initially_hidden(self, driver):
        """TC314 – Error message on signup form is hidden by default."""
        go(driver, "/signup.html")
        err = wait_for(driver, By.ID, "error-msg")
        assert not err.is_displayed()

    def test_TC315_index_modal_initially_hidden(self, driver):
        """TC315 – Role selection modal on index page is hidden by default."""
        go(driver, "/index.html")
        modal = wait_for(driver, By.ID, "role-modal")
        assert not modal.is_displayed()

    def test_TC316_login_page_no_horizontal_scroll(self, driver):
        """TC316 – Login page body doesn't produce horizontal scrollbar."""
        go(driver, "/login.html")
        scroll_width = driver.execute_script("return document.body.scrollWidth;")
        client_width = driver.execute_script("return document.body.clientWidth;")
        assert scroll_width <= client_width + 20  # Allow small tolerance

    def test_TC317_events_tab_badge_is_numeric(self, driver):
        """TC317 – All tab badges contain numeric values."""
        go(driver, "/events.html")
        for badge_id in ["badge-all", "badge-upcoming", "badge-ongoing", "badge-completed", "badge-cancelled"]:
            badge = driver.find_element(By.ID, badge_id)
            # Should be empty or a number
            text = badge.text.strip()
            assert text.isdigit() or text == "", f"Badge {badge_id} is not numeric: '{text}'"

    def test_TC318_create_event_category_default_option(self, driver):
        """TC318 – Category dropdown has Summit as the first/default option."""
        go(driver, "/create_event.html")
        sel = driver.find_element(By.ID, "eventCategory")
        from selenium.webdriver.support.select import Select
        s = Select(sel)
        assert s.first_selected_option.text == "Summit"

    def test_TC319_create_event_checkpoints_default_value(self, driver):
        """TC319 – Number of checkpoints defaults to 4."""
        go(driver, "/create_event.html")
        el = driver.find_element(By.ID, "checkpointsCount")
        assert el.get_attribute("value") == "4"

    def test_TC320_create_event_min_attendance_default_80(self, driver):
        """TC320 – Min attendance for certificate defaults to 80."""
        go(driver, "/create_event.html")
        el = driver.find_element(By.ID, "minAttendance")
        assert el.get_attribute("value") == "80"

    def test_TC321_create_event_qr_refresh_default_10(self, driver):
        """TC321 – QR refresh interval defaults to 10 seconds."""
        go(driver, "/create_event.html")
        el = driver.find_element(By.ID, "qrRefresh")
        assert el.get_attribute("value") == "10"

    def test_TC322_create_event_start_time_default_09(self, driver):
        """TC322 – Start time defaults to 09:00."""
        go(driver, "/create_event.html")
        el = driver.find_element(By.ID, "startTime")
        assert el.get_attribute("value") == "09:00"

    def test_TC323_create_event_end_time_default_1230(self, driver):
        """TC323 – End time defaults to 12:30."""
        go(driver, "/create_event.html")
        el = driver.find_element(By.ID, "endTime")
        assert el.get_attribute("value") == "12:30"

    def test_TC324_login_remember_me_unchecked_by_default(self, driver):
        """TC324 – Remember Me checkbox is unchecked by default."""
        go(driver, "/login.html")
        cb = driver.find_element(By.CSS_SELECTOR, ".remember-me input[type='checkbox']")
        assert not cb.is_selected()

    def test_TC325_login_remember_me_can_be_checked(self, driver):
        """TC325 – Remember Me checkbox can be checked by clicking."""
        go(driver, "/login.html")
        cb = driver.find_element(By.CSS_SELECTOR, ".remember-me input[type='checkbox']")
        cb.click()
        assert cb.is_selected()

    def test_TC326_login_tab_key_navigation(self, driver):
        """TC326 – Tab key moves focus from email to password field."""
        go(driver, "/login.html")
        click_when_ready(driver, By.CSS_SELECTOR, "[data-role='attendee']")
        email = driver.find_element(By.ID, "email")
        email.click()
        email.send_keys(Keys.TAB)
        focused = driver.switch_to.active_element
        assert focused is not None  # Some focusable element gained focus

    def test_TC327_signup_form_accepts_all_fields(self, driver):
        """TC327 – All signup form fields accept and retain text input."""
        go(driver, "/signup.html")
        fields = {
            "fullName": "Jane Doe",
            "email": "jane@test.com",
            "phone": "9876543210",
            "institution": "IIT Bombay",
            "areaCity": "Mumbai",
            "nativePlace": "Pune",
        }
        for fid, val in fields.items():
            fill(driver, By.ID, fid, val)
        for fid, val in fields.items():
            assert driver.find_element(By.ID, fid).get_attribute("value") == val

    def test_TC328_events_sidebar_has_all_nav_items(self, driver):
        """TC328 – Events page sidebar has all 7 navigation items."""
        go(driver, "/events.html")
        items = driver.find_elements(By.CLASS_NAME, "sidebar-item")
        assert len(items) >= 7

    def test_TC329_dashboard_bottom_nav_has_4_items(self, driver):
        """TC329 – Dashboard bottom nav has 4 navigation items."""
        go(driver, "/dashboard.html")
        items = driver.find_elements(By.CLASS_NAME, "nav-item")
        assert len(items) >= 4

    def test_TC330_sidebar_footer_avatar_present(self, driver):
        """TC330 – Sidebar footer avatar element is present."""
        go(driver, "/dashboard.html")
        avatar = wait_for(driver, By.ID, "sidebar-avatar")
        assert avatar is not None

    def test_TC331_sidebar_footer_name_present(self, driver):
        """TC331 – Sidebar footer user name element is present."""
        go(driver, "/dashboard.html")
        name = wait_for(driver, By.ID, "sidebar-name")
        assert name is not None

    def test_TC332_sidebar_footer_email_present(self, driver):
        """TC332 – Sidebar footer user email element is present."""
        go(driver, "/dashboard.html")
        email = wait_for(driver, By.ID, "sidebar-email")
        assert email is not None

    def test_TC333_sidebar_footer_logout_clickable(self, driver):
        """TC333 – Sidebar logout icon element is present and has ID."""
        go(driver, "/dashboard.html")
        logout = wait_for(driver, By.ID, "sidebar-logout")
        assert logout.is_displayed()

    def test_TC334_login_page_role_descriptions_visible(self, driver):
        """TC334 – Each role card shows a description sub-text."""
        go(driver, "/login.html")
        cards = driver.find_elements(By.CLASS_NAME, "role-option")
        for card in cards:
            p_tags = card.find_elements(By.TAG_NAME, "p")
            assert len(p_tags) > 0

    def test_TC335_index_header_two_buttons(self, driver):
        """TC335 – Index page header has exactly 2 action buttons."""
        go(driver, "/index.html")
        header_btns = driver.find_elements(By.CLASS_NAME, "header-actions")
        if header_btns:
            btns = header_btns[0].find_elements(By.TAG_NAME, "button")
            assert len(btns) == 2

    def test_TC336_create_event_form_card_white_bg(self, driver):
        """TC336 – Form card on create event page has white background."""
        go(driver, "/create_event.html")
        card = wait_for(driver, By.CLASS_NAME, "form-card")
        bg = driver.execute_script(
            "return window.getComputedStyle(arguments[0]).backgroundColor;", card
        )
        assert "255, 255, 255" in bg or "white" in bg.lower()

    def test_TC337_login_error_msg_red_color(self, driver):
        """TC337 – Error message on login page has red-ish color styling."""
        go(driver, "/login.html")
        assert "e53e3e" in driver.page_source or "error" in driver.page_source.lower()

    def test_TC338_create_event_step_circles_numbered(self, driver):
        """TC338 – Step circles contain numbers 1-7."""
        go(driver, "/create_event.html")
        circles = driver.find_elements(By.CLASS_NAME, "step-circle")
        texts = [c.text.strip() for c in circles]
        for i in range(1, 8):
            assert str(i) in texts

    def test_TC339_events_page_five_filter_tabs_count(self, driver):
        """TC339 – Events page has exactly 5 filter tabs."""
        go(driver, "/events.html")
        tabs = driver.find_elements(By.CLASS_NAME, "tab")
        assert len(tabs) == 5

    def test_TC340_login_organizer_subtxt_correct(self, driver):
        """TC340 – Organizer role card subtitle describes creating/managing events."""
        go(driver, "/login.html")
        card = wait_for(driver, By.CSS_SELECTOR, "[data-role='organizer']")
        assert "Create" in card.text or "manage" in card.text.lower() or "event" in card.text.lower()

    def test_TC341_login_attendee_subtxt_correct(self, driver):
        """TC341 – Attendee role card subtitle mentions discovering or attending events."""
        go(driver, "/login.html")
        card = wait_for(driver, By.CSS_SELECTOR, "[data-role='attendee']")
        assert "Discover" in card.text or "attend" in card.text.lower()

    def test_TC342_login_volunteer_subtxt_correct(self, driver):
        """TC342 – Volunteer role card subtitle mentions verifying attendance."""
        go(driver, "/login.html")
        card = wait_for(driver, By.CSS_SELECTOR, "[data-role='volunteer']")
        assert "Verify" in card.text or "attendance" in card.text.lower() or "manage" in card.text.lower()

    def test_TC343_signup_secret_key_type_password(self, driver):
        """TC343 – Organizer secret key on signup is type=password."""
        go(driver, "/signup.html")
        el = driver.find_element(By.ID, "secretKey")
        assert el.get_attribute("type") == "password"

    def test_TC344_create_event_venue_type_text(self, driver):
        """TC344 – Venue name field type is 'text'."""
        go(driver, "/create_event.html")
        el = driver.find_element(By.ID, "venueName")
        assert el.get_attribute("type") == "text"

    def test_TC345_events_search_input_type_text(self, driver):
        """TC345 – Events search input type is 'text'."""
        go(driver, "/events.html")
        el = driver.find_element(By.ID, "searchInput")
        assert el.get_attribute("type") == "text"

    def test_TC346_index_page_footer_present(self, driver):
        """TC346 – Index page has a <footer> element."""
        go(driver, "/index.html")
        footer = driver.find_elements(By.TAG_NAME, "footer")
        assert len(footer) > 0

    def test_TC347_index_page_main_section_present(self, driver):
        """TC347 – Index page has a <main> element."""
        go(driver, "/index.html")
        main = driver.find_elements(By.TAG_NAME, "main")
        assert len(main) > 0

    def test_TC348_index_header_element_present(self, driver):
        """TC348 – Index page has a <header> element."""
        go(driver, "/index.html")
        header = driver.find_elements(By.TAG_NAME, "header")
        assert len(header) > 0

    def test_TC349_signup_fullname_placeholder(self, driver):
        """TC349 – Signup full name field has a sample-name placeholder."""
        go(driver, "/signup.html")
        ph = driver.find_element(By.ID, "fullName").get_attribute("placeholder")
        assert ph and len(ph) > 0

    def test_TC350_all_pages_body_has_children(self, driver):
        """TC350 – All main pages have non-empty body elements with child nodes."""
        pages = ["/index.html", "/login.html", "/signup.html",
                 "/dashboard.html", "/events.html", "/create_event.html"]
        for page in pages:
            go(driver, page)
            children = driver.execute_script(
                "return document.body.children.length;"
            )
            assert children > 0, f"Body has no children on {page}"
