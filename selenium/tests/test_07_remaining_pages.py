"""
test_07_participants_volunteers_live_certs_settings.py
TC201 – TC280  (Participants, Volunteers, Live, Certificates, Settings, Attendee pages)
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from conftest import go, wait_for, click_when_ready, fill


# ─── PARTICIPANTS (TC201-TC220) ───────────────────────────────────────────────
class TestParticipantsPage:

    def test_TC201_participants_page_loads(self, driver):
        """TC201 – Participants page loads."""
        go(driver, "/participants.html")
        assert "ZyntraPass" in driver.title or "Participants" in driver.page_source

    def test_TC202_participants_top_bar_present(self, driver):
        """TC202 – Top bar is present on participants page."""
        go(driver, "/participants.html")
        top = driver.find_elements(By.CLASS_NAME, "top-bar")
        assert len(top) > 0

    def test_TC203_participants_sidebar_present(self, driver):
        """TC203 – Sidebar is present on participants page."""
        go(driver, "/participants.html")
        sidebar = driver.find_elements(By.ID, "sidebar")
        assert len(sidebar) > 0

    def test_TC204_participants_bottom_nav_present(self, driver):
        """TC204 – Bottom nav is present on participants page."""
        go(driver, "/participants.html")
        nav = driver.find_elements(By.CLASS_NAME, "bottom-nav")
        assert len(nav) > 0

    def test_TC205_participants_heading_visible(self, driver):
        """TC205 – Participants page has a main heading."""
        go(driver, "/participants.html")
        headings = driver.find_elements(By.TAG_NAME, "h1")
        assert len(headings) > 0 and headings[0].is_displayed()

    def test_TC206_participants_supabase_included(self, driver):
        """TC206 – Supabase script is referenced on participants page."""
        go(driver, "/participants.html")
        assert "supabase" in driver.page_source.lower()

    def test_TC207_participants_sidebar_has_participants_active(self, driver):
        """TC207 – Sidebar marks Participants as active on this page."""
        go(driver, "/participants.html")
        links = driver.find_elements(By.CLASS_NAME, "sidebar-item")
        active_links = [l for l in links if "Participants" in l.text and "active" in l.get_attribute("class")]
        assert len(active_links) > 0

    def test_TC208_participants_page_title_correct(self, driver):
        """TC208 – Page <title> contains 'Participants' or 'ZyntraPass'."""
        go(driver, "/participants.html")
        assert "Participants" in driver.title or "ZyntraPass" in driver.title

    def test_TC209_participants_container_present(self, driver):
        """TC209 – Main container div is present."""
        go(driver, "/participants.html")
        containers = driver.find_elements(By.CLASS_NAME, "container")
        assert len(containers) > 0

    def test_TC210_participants_menu_btn_present(self, driver):
        """TC210 – Menu/hamburger button is present on participants page."""
        go(driver, "/participants.html")
        btns = driver.find_elements(By.CLASS_NAME, "menu-btn")
        assert len(btns) > 0


# ─── VOLUNTEERS (TC211-TC225) ─────────────────────────────────────────────────
class TestVolunteersPage:

    def test_TC211_volunteers_page_loads(self, driver):
        """TC211 – Volunteers page loads successfully."""
        go(driver, "/volunteers.html")
        assert "ZyntraPass" in driver.title or "Volunteer" in driver.page_source

    def test_TC212_volunteers_heading_present(self, driver):
        """TC212 – Volunteers page has a main heading."""
        go(driver, "/volunteers.html")
        headings = driver.find_elements(By.TAG_NAME, "h1")
        assert len(headings) > 0

    def test_TC213_volunteers_sidebar_present(self, driver):
        """TC213 – Sidebar is present on volunteers page."""
        go(driver, "/volunteers.html")
        assert len(driver.find_elements(By.ID, "sidebar")) > 0

    def test_TC214_volunteers_top_bar_present(self, driver):
        """TC214 – Top bar is present on volunteers page."""
        go(driver, "/volunteers.html")
        assert len(driver.find_elements(By.CLASS_NAME, "top-bar")) > 0

    def test_TC215_volunteers_bottom_nav_present(self, driver):
        """TC215 – Bottom nav is present on volunteers page."""
        go(driver, "/volunteers.html")
        assert len(driver.find_elements(By.CLASS_NAME, "bottom-nav")) > 0

    def test_TC216_volunteers_supabase_included(self, driver):
        """TC216 – Supabase CDN is referenced on volunteers page."""
        go(driver, "/volunteers.html")
        assert "supabase" in driver.page_source.lower()

    def test_TC217_volunteers_sidebar_volunteers_active(self, driver):
        """TC217 – Sidebar marks Volunteers as active on this page."""
        go(driver, "/volunteers.html")
        links = driver.find_elements(By.CLASS_NAME, "sidebar-item")
        active = [l for l in links if "Volunteers" in l.text and "active" in l.get_attribute("class")]
        assert len(active) > 0

    def test_TC218_volunteer_dashboard_page_loads(self, driver):
        """TC218 – Volunteer dashboard page loads."""
        go(driver, "/volunteer_dashboard.html")
        assert "ZyntraPass" in driver.page_source or "Volunteer" in driver.page_source

    def test_TC219_volunteer_scan_page_loads(self, driver):
        """TC219 – Volunteer scan page loads."""
        go(driver, "/volunteer_scan.html")
        assert "ZyntraPass" in driver.page_source or "scan" in driver.page_source.lower()

    def test_TC220_volunteer_participants_page_loads(self, driver):
        """TC220 – Volunteer participants page loads."""
        go(driver, "/volunteer_participants.html")
        assert "ZyntraPass" in driver.page_source or "participant" in driver.page_source.lower()


# ─── LIVE ATTENDANCE (TC221-TC235) ───────────────────────────────────────────
class TestLiveAttendancePage:

    def test_TC221_live_page_loads(self, driver):
        """TC221 – Live Attendance page loads."""
        go(driver, "/live.html")
        assert "ZyntraPass" in driver.page_source

    def test_TC222_live_page_top_bar(self, driver):
        """TC222 – Top bar is present on live page."""
        go(driver, "/live.html")
        assert len(driver.find_elements(By.CLASS_NAME, "top-bar")) > 0

    def test_TC223_live_page_sidebar_present(self, driver):
        """TC223 – Sidebar is present on live page."""
        go(driver, "/live.html")
        assert len(driver.find_elements(By.ID, "sidebar")) > 0

    def test_TC224_live_page_bottom_nav_present(self, driver):
        """TC224 – Bottom nav is present on live page."""
        go(driver, "/live.html")
        assert len(driver.find_elements(By.CLASS_NAME, "bottom-nav")) > 0

    def test_TC225_live_sidebar_live_active(self, driver):
        """TC225 – Sidebar marks Live Attendance as active on this page."""
        go(driver, "/live.html")
        links = driver.find_elements(By.CLASS_NAME, "sidebar-item")
        active = [l for l in links if "Live" in l.text and "active" in l.get_attribute("class")]
        assert len(active) > 0

    def test_TC226_live_page_supabase_included(self, driver):
        """TC226 – Supabase CDN is referenced on live page."""
        go(driver, "/live.html")
        assert "supabase" in driver.page_source.lower()

    def test_TC227_live_page_has_heading(self, driver):
        """TC227 – Live page has a visible heading."""
        go(driver, "/live.html")
        headings = driver.find_elements(By.TAG_NAME, "h1")
        assert len(headings) > 0

    def test_TC228_live_bottom_nav_live_active(self, driver):
        """TC228 – Bottom nav marks 'Live' as active on the live page."""
        go(driver, "/live.html")
        items = driver.find_elements(By.CLASS_NAME, "nav-item")
        active = [i for i in items if "Live" in i.text and "active" in i.get_attribute("class")]
        assert len(active) > 0


# ─── CERTIFICATES (TC229-TC242) ──────────────────────────────────────────────
class TestCertificatesPage:

    def test_TC229_certificates_page_loads(self, driver):
        """TC229 – Certificates page loads."""
        go(driver, "/certificates.html")
        assert "ZyntraPass" in driver.page_source or "Certificates" in driver.page_source

    def test_TC230_certificates_heading_present(self, driver):
        """TC230 – Certificates page has a main heading."""
        go(driver, "/certificates.html")
        headings = driver.find_elements(By.TAG_NAME, "h1")
        assert len(headings) > 0

    def test_TC231_certificates_top_bar_present(self, driver):
        """TC231 – Top bar is present on certificates page."""
        go(driver, "/certificates.html")
        assert len(driver.find_elements(By.CLASS_NAME, "top-bar")) > 0

    def test_TC232_certificates_sidebar_present(self, driver):
        """TC232 – Sidebar is present on certificates page."""
        go(driver, "/certificates.html")
        assert len(driver.find_elements(By.ID, "sidebar")) > 0

    def test_TC233_certificates_bottom_nav_present(self, driver):
        """TC233 – Bottom nav is present on certificates page."""
        go(driver, "/certificates.html")
        assert len(driver.find_elements(By.CLASS_NAME, "bottom-nav")) > 0

    def test_TC234_certificates_sidebar_active(self, driver):
        """TC234 – Sidebar marks Certificates as active."""
        go(driver, "/certificates.html")
        links = driver.find_elements(By.CLASS_NAME, "sidebar-item")
        active = [l for l in links if "Certificates" in l.text and "active" in l.get_attribute("class")]
        assert len(active) > 0

    def test_TC235_certificates_supabase_included(self, driver):
        """TC235 – Supabase CDN is referenced on certificates page."""
        go(driver, "/certificates.html")
        assert "supabase" in driver.page_source.lower()


# ─── SETTINGS (TC236-TC250) ──────────────────────────────────────────────────
class TestSettingsPage:

    def test_TC236_settings_page_loads(self, driver):
        """TC236 – Settings page loads."""
        go(driver, "/settings.html")
        assert "ZyntraPass" in driver.page_source or "Settings" in driver.page_source

    def test_TC237_settings_heading_present(self, driver):
        """TC237 – Settings page has a main heading."""
        go(driver, "/settings.html")
        headings = driver.find_elements(By.TAG_NAME, "h1")
        assert len(headings) > 0

    def test_TC238_settings_top_bar_present(self, driver):
        """TC238 – Top bar is present on settings page."""
        go(driver, "/settings.html")
        assert len(driver.find_elements(By.CLASS_NAME, "top-bar")) > 0

    def test_TC239_settings_sidebar_present(self, driver):
        """TC239 – Sidebar is present on settings page."""
        go(driver, "/settings.html")
        assert len(driver.find_elements(By.ID, "sidebar")) > 0

    def test_TC240_settings_bottom_nav_present(self, driver):
        """TC240 – Bottom nav is present on settings page."""
        go(driver, "/settings.html")
        assert len(driver.find_elements(By.CLASS_NAME, "bottom-nav")) > 0

    def test_TC241_settings_sidebar_settings_active(self, driver):
        """TC241 – Sidebar marks Settings as active."""
        go(driver, "/settings.html")
        links = driver.find_elements(By.CLASS_NAME, "sidebar-item")
        active = [l for l in links if "Settings" in l.text and "active" in l.get_attribute("class")]
        assert len(active) > 0

    def test_TC242_settings_supabase_included(self, driver):
        """TC242 – Supabase CDN is referenced on settings page."""
        go(driver, "/settings.html")
        assert "supabase" in driver.page_source.lower()


# ─── ATTENDEE DASHBOARD (TC243-TC260) ────────────────────────────────────────
class TestAttendeeDashboard:

    def test_TC243_attendee_dashboard_loads(self, driver):
        """TC243 – Attendee dashboard page loads."""
        go(driver, "/attendee_dashboard.html")
        assert "ZyntraPass" in driver.page_source

    def test_TC244_attendee_dashboard_has_heading(self, driver):
        """TC244 – Attendee dashboard has a heading."""
        go(driver, "/attendee_dashboard.html")
        headings = driver.find_elements(By.TAG_NAME, "h1")
        assert len(headings) > 0

    def test_TC245_attendee_discover_page_loads(self, driver):
        """TC245 – Attendee Discover page loads."""
        go(driver, "/attendee_discover.html")
        assert "ZyntraPass" in driver.page_source

    def test_TC246_attendee_my_events_page_loads(self, driver):
        """TC246 – Attendee My Events page loads."""
        go(driver, "/attendee_my_events.html")
        assert "ZyntraPass" in driver.page_source

    def test_TC247_attendee_attendance_page_loads(self, driver):
        """TC247 – Attendee Attendance page loads."""
        go(driver, "/attendee_attendance.html")
        assert "ZyntraPass" in driver.page_source

    def test_TC248_attendee_certs_page_loads(self, driver):
        """TC248 – Attendee Certificates page loads."""
        go(driver, "/attendee_certificates.html")
        assert "ZyntraPass" in driver.page_source

    def test_TC249_attendee_settings_page_loads(self, driver):
        """TC249 – Attendee Settings page loads."""
        go(driver, "/attendee_settings.html")
        assert "ZyntraPass" in driver.page_source

    def test_TC250_attendee_signup_page_loads(self, driver):
        """TC250 – Attendee Signup page loads."""
        go(driver, "/attendee_signup.html")
        assert "ZyntraPass" in driver.page_source


# ─── MULTI-TAB NAVIGATION FLOW (TC251-TC280) ─────────────────────────────────
class TestMultiTabNavigation:

    def test_TC251_open_login_in_new_tab(self, driver):
        """TC251 – Login page can be opened in a new browser tab."""
        driver.execute_script("window.open(arguments[0]);", "about:blank")
        driver.switch_to.window(driver.window_handles[-1])
        go(driver, "/login.html")
        assert "ZyntraPass" in driver.title or "login" in driver.current_url
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    def test_TC252_open_events_in_new_tab(self, driver):
        """TC252 – Events page can be opened in a second browser tab."""
        driver.execute_script("window.open(arguments[0]);", "about:blank")
        driver.switch_to.window(driver.window_handles[-1])
        go(driver, "/events.html")
        assert "Events" in driver.page_source or "ZyntraPass" in driver.page_source
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    def test_TC253_switch_between_tabs(self, driver):
        """TC253 – Browser correctly switches between two open tabs."""
        original = driver.current_window_handle
        go(driver, "/index.html")
        driver.execute_script("window.open(arguments[0]);", "about:blank")
        driver.switch_to.window(driver.window_handles[-1])
        go(driver, "/login.html")
        assert "login" in driver.current_url
        driver.switch_to.window(original)
        assert "index" in driver.current_url or driver.current_url.endswith("/")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    def test_TC254_index_signin_opens_login(self, driver):
        """TC254 – Sign In button on index opens login in same tab."""
        go(driver, "/index.html")
        click_when_ready(driver, By.ID, "sign-in-btn")
        WebDriverWait(driver, 10).until(EC.url_contains("login"))
        assert "login" in driver.current_url

    def test_TC255_login_to_signup_back_to_login(self, driver):
        """TC255 – User can navigate login → signup → back to login."""
        go(driver, "/login.html")
        click_when_ready(driver, By.CSS_SELECTOR, "[data-role='attendee']")
        click_when_ready(driver, By.ID, "create-account-link")
        WebDriverWait(driver, 10).until(EC.url_contains("signup"))
        driver.find_element(By.LINK_TEXT, "Sign in").click()
        WebDriverWait(driver, 10).until(EC.url_contains("login"))
        assert "login" in driver.current_url

    def test_TC256_dashboard_sidebar_events_navigation(self, driver):
        """TC256 – Sidebar Events link on dashboard navigates to events.html."""
        go(driver, "/dashboard.html")
        links = driver.find_elements(By.CLASS_NAME, "sidebar-item")
        event_links = [l for l in links if "Events" in l.text]
        if event_links:
            event_links[0].click()
            WebDriverWait(driver, 10).until(EC.url_contains("events"))
            assert "events" in driver.current_url

    def test_TC257_events_sidebar_participants_navigation(self, driver):
        """TC257 – Sidebar Participants link on events page navigates to participants.html."""
        go(driver, "/events.html")
        links = driver.find_elements(By.CLASS_NAME, "sidebar-item")
        p_links = [l for l in links if "Participants" in l.text]
        if p_links:
            p_links[0].click()
            WebDriverWait(driver, 10).until(EC.url_contains("participants"))
            assert "participants" in driver.current_url

    def test_TC258_dashboard_sidebar_certificates_navigation(self, driver):
        """TC258 – Sidebar Certificates link navigates to certificates.html."""
        go(driver, "/dashboard.html")
        links = driver.find_elements(By.CLASS_NAME, "sidebar-item")
        c_links = [l for l in links if "Certificates" in l.text]
        if c_links:
            c_links[0].click()
            WebDriverWait(driver, 10).until(EC.url_contains("certificates"))
            assert "certificates" in driver.current_url

    def test_TC259_dashboard_sidebar_settings_navigation(self, driver):
        """TC259 – Sidebar Settings link navigates to settings.html."""
        go(driver, "/dashboard.html")
        links = driver.find_elements(By.CLASS_NAME, "sidebar-item")
        s_links = [l for l in links if "Settings" in l.text]
        if s_links:
            s_links[0].click()
            WebDriverWait(driver, 10).until(EC.url_contains("settings"))
            assert "settings" in driver.current_url

    def test_TC260_dashboard_sidebar_volunteers_navigation(self, driver):
        """TC260 – Sidebar Volunteers link navigates to volunteers.html."""
        go(driver, "/dashboard.html")
        links = driver.find_elements(By.CLASS_NAME, "sidebar-item")
        v_links = [l for l in links if "Volunteers" in l.text]
        if v_links:
            v_links[0].click()
            WebDriverWait(driver, 10).until(EC.url_contains("volunteers"))
            assert "volunteers" in driver.current_url

    def test_TC261_dashboard_sidebar_live_navigation(self, driver):
        """TC261 – Sidebar Live Attendance link navigates to live.html."""
        go(driver, "/dashboard.html")
        links = driver.find_elements(By.CLASS_NAME, "sidebar-item")
        live_links = [l for l in links if "Live" in l.text]
        if live_links:
            live_links[0].click()
            WebDriverWait(driver, 10).until(EC.url_contains("live"))
            assert "live" in driver.current_url

    def test_TC262_events_create_event_back_to_events(self, driver):
        """TC262 – Create Event Back button returns from create_event to dashboard."""
        go(driver, "/create_event.html")
        back_btns = driver.find_elements(By.CLASS_NAME, "btn-back")
        if back_btns:
            back_btns[0].click()
            WebDriverWait(driver, 10).until(EC.url_contains("dashboard"))
            assert "dashboard" in driver.current_url

    def test_TC263_signup_returns_to_login(self, driver):
        """TC263 – Clicking 'Sign in' on signup page returns to login.html."""
        go(driver, "/signup.html")
        driver.find_element(By.LINK_TEXT, "Sign in").click()
        WebDriverWait(driver, 10).until(EC.url_contains("login"))
        assert "login" in driver.current_url

    def test_TC264_attendee_dashboard_discover_link(self, driver):
        """TC264 – Attendee dashboard links to Discover page."""
        go(driver, "/attendee_dashboard.html")
        assert "attendee_discover" in driver.page_source or "Discover" in driver.page_source

    def test_TC265_attendee_dashboard_my_events_link(self, driver):
        """TC265 – Attendee dashboard has My Events link reference."""
        go(driver, "/attendee_dashboard.html")
        assert "attendee_my_events" in driver.page_source or "My Events" in driver.page_source

    def test_TC266_all_pages_have_supabase(self, driver):
        """TC266 – All key pages include Supabase CDN script."""
        pages = ["/login.html", "/dashboard.html", "/events.html",
                 "/participants.html", "/certificates.html", "/settings.html"]
        for page in pages:
            go(driver, page)
            assert "supabase" in driver.page_source.lower(), f"Supabase missing on {page}"

    def test_TC267_all_pages_include_inter_font_or_css(self, driver):
        """TC267 – Key pages include Inter font or CSS link."""
        pages = ["/dashboard.html", "/events.html", "/create_event.html"]
        for page in pages:
            go(driver, page)
            assert "Inter" in driver.page_source or "font" in driver.page_source.lower()

    def test_TC268_navigation_bottom_dashboard_link(self, driver):
        """TC268 – Bottom nav Dashboard link on events page works."""
        go(driver, "/events.html")
        nav_items = driver.find_elements(By.CLASS_NAME, "nav-item")
        dash_links = [n for n in nav_items if "Dashboard" in n.text]
        if dash_links:
            dash_links[0].click()
            WebDriverWait(driver, 10).until(EC.url_contains("dashboard"))
            assert "dashboard" in driver.current_url

    def test_TC269_navigation_bottom_participants_link(self, driver):
        """TC269 – Bottom nav Participants link works."""
        go(driver, "/events.html")
        nav_items = driver.find_elements(By.CLASS_NAME, "nav-item")
        p_links = [n for n in nav_items if "Participants" in n.text]
        if p_links:
            p_links[0].click()
            WebDriverWait(driver, 10).until(EC.url_contains("participants"))
            assert "participants" in driver.current_url

    def test_TC270_navigation_bottom_live_link(self, driver):
        """TC270 – Bottom nav Live link on events page works."""
        go(driver, "/events.html")
        nav_items = driver.find_elements(By.CLASS_NAME, "nav-item")
        live_links = [n for n in nav_items if "Live" in n.text]
        if live_links:
            live_links[0].click()
            WebDriverWait(driver, 10).until(EC.url_contains("live"))
            assert "live" in driver.current_url

    def test_TC271_attendee_settings_supabase_included(self, driver):
        """TC271 – Attendee settings page includes Supabase CDN."""
        go(driver, "/attendee_settings.html")
        assert "supabase" in driver.page_source.lower()

    def test_TC272_attendee_attendance_supabase_included(self, driver):
        """TC272 – Attendee attendance page includes Supabase CDN."""
        go(driver, "/attendee_attendance.html")
        assert "supabase" in driver.page_source.lower()

    def test_TC273_attendee_discover_supabase_included(self, driver):
        """TC273 – Attendee Discover page includes Supabase CDN."""
        go(driver, "/attendee_discover.html")
        assert "supabase" in driver.page_source.lower()

    def test_TC274_attendee_my_events_supabase_included(self, driver):
        """TC274 – Attendee My Events page includes Supabase CDN."""
        go(driver, "/attendee_my_events.html")
        assert "supabase" in driver.page_source.lower()

    def test_TC275_volunteer_dashboard_supabase_included(self, driver):
        """TC275 – Volunteer dashboard page includes Supabase CDN."""
        go(driver, "/volunteer_dashboard.html")
        assert "supabase" in driver.page_source.lower()

    def test_TC276_index_page_responsive_viewport_meta(self, driver):
        """TC276 – Index page has responsive viewport meta tag."""
        go(driver, "/index.html")
        assert "viewport" in driver.page_source

    def test_TC277_login_page_responsive_viewport_meta(self, driver):
        """TC277 – Login page has responsive viewport meta tag."""
        go(driver, "/login.html")
        assert "viewport" in driver.page_source

    def test_TC278_create_event_page_responsive(self, driver):
        """TC278 – Create event page has responsive viewport meta tag."""
        go(driver, "/create_event.html")
        assert "viewport" in driver.page_source

    def test_TC279_all_role_pages_return_200(self, driver):
        """TC279 – All main role-specific pages load without HTTP error."""
        pages = [
            "/dashboard.html", "/attendee_dashboard.html",
            "/volunteer_dashboard.html", "/events.html"
        ]
        for p in pages:
            go(driver, p)
            assert "404" not in driver.title and "error" not in driver.title.lower()

    def test_TC280_page_source_not_empty_on_all_pages(self, driver):
        """TC280 – Page source is not empty for all main pages."""
        pages = ["/index.html", "/login.html", "/signup.html",
                 "/dashboard.html", "/events.html"]
        for p in pages:
            go(driver, p)
            assert len(driver.page_source) > 100
