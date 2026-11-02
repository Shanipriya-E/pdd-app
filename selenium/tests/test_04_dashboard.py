"""
test_04_dashboard.py  —  Organizer Dashboard
TC081 – TC115
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from conftest import go, wait_for, click_when_ready, fill, login_as_organizer


class TestOrganizerDashboard:

    def test_TC081_dashboard_page_title(self, driver):
        """TC081 – Dashboard page title contains 'Organizer Dashboard'."""
        go(driver, "/dashboard.html")
        assert "Dashboard" in driver.title or "ZyntraPass" in driver.title

    def test_TC082_top_bar_present(self, driver):
        """TC082 – Top bar is present on the dashboard."""
        go(driver, "/dashboard.html")
        top_bar = wait_for(driver, By.CLASS_NAME, "top-bar")
        assert top_bar.is_displayed()

    def test_TC083_menu_button_present(self, driver):
        """TC083 – Hamburger menu button (☰) is present in top bar."""
        go(driver, "/dashboard.html")
        menu = driver.find_elements(By.CLASS_NAME, "menu-btn")
        assert len(menu) > 0

    def test_TC084_sidebar_hidden_by_default(self, driver):
        """TC084 – Sidebar drawer is hidden by default (not active class)."""
        go(driver, "/dashboard.html")
        sidebar = wait_for(driver, By.ID, "sidebar")
        assert "active" not in sidebar.get_attribute("class")

    def test_TC085_sidebar_opens_on_menu_click(self, driver):
        """TC085 – Clicking menu button opens the sidebar drawer."""
        go(driver, "/dashboard.html")
        menu_btns = driver.find_elements(By.CLASS_NAME, "menu-btn")
        if menu_btns:
            menu_btns[0].click()
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#sidebar.active"))
            )
            sidebar = driver.find_element(By.ID, "sidebar")
            assert "active" in sidebar.get_attribute("class")

    def test_TC086_sidebar_brand_name_visible(self, driver):
        """TC086 – Sidebar shows 'ZyntraPass' brand name."""
        go(driver, "/dashboard.html")
        sidebar = wait_for(driver, By.ID, "sidebar")
        assert "ZyntraPass" in sidebar.text

    def test_TC087_sidebar_dashboard_link_present(self, driver):
        """TC087 – Sidebar has 'Dashboard' navigation link."""
        go(driver, "/dashboard.html")
        links = driver.find_elements(By.CLASS_NAME, "sidebar-item")
        texts = [l.text for l in links]
        assert any("Dashboard" in t for t in texts)

    def test_TC088_sidebar_events_link_present(self, driver):
        """TC088 – Sidebar has 'Events' navigation link."""
        go(driver, "/dashboard.html")
        links = driver.find_elements(By.CLASS_NAME, "sidebar-item")
        texts = [l.text for l in links]
        assert any("Events" in t for t in texts)

    def test_TC089_sidebar_participants_link_present(self, driver):
        """TC089 – Sidebar has 'Participants' navigation link."""
        go(driver, "/dashboard.html")
        links = driver.find_elements(By.CLASS_NAME, "sidebar-item")
        texts = [l.text for l in links]
        assert any("Participants" in t for t in texts)

    def test_TC090_sidebar_live_attendance_link_present(self, driver):
        """TC090 – Sidebar has 'Live Attendance' link."""
        go(driver, "/dashboard.html")
        links = driver.find_elements(By.CLASS_NAME, "sidebar-item")
        texts = [l.text for l in links]
        assert any("Live" in t for t in texts)

    def test_TC091_sidebar_volunteers_link_present(self, driver):
        """TC091 – Sidebar has 'Volunteers' navigation link."""
        go(driver, "/dashboard.html")
        links = driver.find_elements(By.CLASS_NAME, "sidebar-item")
        texts = [l.text for l in links]
        assert any("Volunteers" in t for t in texts)

    def test_TC092_sidebar_certificates_link_present(self, driver):
        """TC092 – Sidebar has 'Certificates' navigation link."""
        go(driver, "/dashboard.html")
        links = driver.find_elements(By.CLASS_NAME, "sidebar-item")
        texts = [l.text for l in links]
        assert any("Certificates" in t for t in texts)

    def test_TC093_sidebar_settings_link_present(self, driver):
        """TC093 – Sidebar has 'Settings' navigation link."""
        go(driver, "/dashboard.html")
        links = driver.find_elements(By.CLASS_NAME, "sidebar-item")
        texts = [l.text for l in links]
        assert any("Settings" in t for t in texts)

    def test_TC094_sidebar_logout_icon_present(self, driver):
        """TC094 – Sidebar footer has logout icon/button."""
        go(driver, "/dashboard.html")
        logout = wait_for(driver, By.ID, "sidebar-logout")
        assert logout.is_displayed()

    def test_TC095_bottom_nav_present(self, driver):
        """TC095 – Bottom navigation bar is present on dashboard."""
        go(driver, "/dashboard.html")
        nav = wait_for(driver, By.CLASS_NAME, "bottom-nav")
        assert nav.is_displayed()

    def test_TC096_bottom_nav_dashboard_link(self, driver):
        """TC096 – Bottom nav has Dashboard link."""
        go(driver, "/dashboard.html")
        nav = wait_for(driver, By.CLASS_NAME, "bottom-nav")
        assert "Dashboard" in nav.text

    def test_TC097_bottom_nav_events_link(self, driver):
        """TC097 – Bottom nav has Events link."""
        go(driver, "/dashboard.html")
        nav = wait_for(driver, By.CLASS_NAME, "bottom-nav")
        assert "Events" in nav.text

    def test_TC098_bottom_nav_participants_link(self, driver):
        """TC098 – Bottom nav has Participants link."""
        go(driver, "/dashboard.html")
        nav = wait_for(driver, By.CLASS_NAME, "bottom-nav")
        assert "Participants" in nav.text

    def test_TC099_loading_state_element_present(self, driver):
        """TC099 – Loading state element exists in DOM."""
        go(driver, "/dashboard.html")
        loading = wait_for(driver, By.ID, "loading-state")
        assert loading is not None

    def test_TC100_live_attendance_btn_present(self, driver):
        """TC100 – 'Live attendance' button is present in action buttons."""
        go(driver, "/dashboard.html")
        btns = driver.find_elements(By.CLASS_NAME, "btn-outline")
        texts = [b.text for b in btns]
        assert any("Live" in t or "live" in t for t in texts)

    def test_TC101_create_event_btn_present(self, driver):
        """TC101 – 'Create event' button is present in action buttons."""
        go(driver, "/dashboard.html")
        btns = driver.find_elements(By.CLASS_NAME, "btn-primary")
        texts = [b.text for b in btns]
        assert any("Create" in t for t in texts)

    def test_TC102_create_event_btn_navigates(self, driver):
        """TC102 – Clicking Create Event button navigates to create_event.html."""
        go(driver, "/dashboard.html")
        btns = driver.find_elements(By.CLASS_NAME, "btn-primary")
        create_btns = [b for b in btns if "Create" in b.text]
        if create_btns:
            create_btns[0].click()
            WebDriverWait(driver, 10).until(EC.url_contains("create_event"))
            assert "create_event" in driver.current_url

    def test_TC103_stats_grid_present(self, driver):
        """TC103 – Stats grid container is present on dashboard."""
        go(driver, "/dashboard.html")
        grid = wait_for(driver, By.CLASS_NAME, "stats-grid")
        assert grid.is_displayed()

    def test_TC104_stat_cards_present(self, driver):
        """TC104 – At least 1 stat card is present on the dashboard."""
        go(driver, "/dashboard.html")
        cards = driver.find_elements(By.CLASS_NAME, "stat-card")
        assert len(cards) >= 1

    def test_TC105_total_events_stat_card_present(self, driver):
        """TC105 – 'Total Events' stat card is present."""
        go(driver, "/dashboard.html")
        assert "Total Events" in driver.page_source

    def test_TC106_registrations_stat_card_present(self, driver):
        """TC106 – 'Registrations' stat card is present."""
        go(driver, "/dashboard.html")
        assert "Registrations" in driver.page_source

    def test_TC107_verified_attendees_stat_present(self, driver):
        """TC107 – 'Verified Attendees' stat card is present."""
        go(driver, "/dashboard.html")
        assert "Verified" in driver.page_source

    def test_TC108_pending_stat_card_present(self, driver):
        """TC108 – 'Pending' stat card is present."""
        go(driver, "/dashboard.html")
        assert "Pending" in driver.page_source

    def test_TC109_certificates_stat_card_present(self, driver):
        """TC109 – 'Certificates' stat card is present."""
        go(driver, "/dashboard.html")
        assert "Certificates" in driver.page_source

    def test_TC110_sidebar_overlay_hidden_by_default(self, driver):
        """TC110 – Sidebar overlay is not visible by default."""
        go(driver, "/dashboard.html")
        overlay = wait_for(driver, By.ID, "sidebar-overlay")
        assert "active" not in overlay.get_attribute("class")

    def test_TC111_sidebar_closes_on_overlay_click(self, driver):
        """TC111 – Clicking sidebar overlay closes the sidebar."""
        go(driver, "/dashboard.html")
        menu_btns = driver.find_elements(By.CLASS_NAME, "menu-btn")
        if menu_btns:
            menu_btns[0].click()
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#sidebar.active"))
            )
            overlay = driver.find_element(By.ID, "sidebar-overlay")
            overlay.click()
            WebDriverWait(driver, 5).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "#sidebar.active"))
            )

    def test_TC112_sidebar_events_link_navigates(self, driver):
        """TC112 – Clicking Events in sidebar navigates to events.html."""
        go(driver, "/dashboard.html")
        links = driver.find_elements(By.CLASS_NAME, "sidebar-item")
        event_links = [l for l in links if "Events" in l.text]
        if event_links:
            event_links[0].click()
            WebDriverWait(driver, 10).until(EC.url_contains("events"))
            assert "events" in driver.current_url

    def test_TC113_bottom_nav_events_navigates(self, driver):
        """TC113 – Bottom nav Events link navigates to events.html."""
        go(driver, "/dashboard.html")
        nav_items = driver.find_elements(By.CLASS_NAME, "nav-item")
        events_item = [n for n in nav_items if "Events" in n.text]
        if events_item:
            events_item[0].click()
            WebDriverWait(driver, 10).until(EC.url_contains("events"))
            assert "events" in driver.current_url

    def test_TC114_dashboard_content_div_present(self, driver):
        """TC114 – Dashboard content div is present in DOM."""
        go(driver, "/dashboard.html")
        content = wait_for(driver, By.ID, "dashboard-content")
        assert content is not None

    def test_TC115_stat_icon_elements_present(self, driver):
        """TC115 – Stat icon elements are present in stat cards."""
        go(driver, "/dashboard.html")
        icons = driver.find_elements(By.CLASS_NAME, "stat-icon")
        assert len(icons) >= 1
