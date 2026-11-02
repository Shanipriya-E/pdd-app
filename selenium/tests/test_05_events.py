"""
test_05_events.py  —  Events Page
TC116 – TC150
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from conftest import go, wait_for, click_when_ready, fill


class TestEventsPage:

    def test_TC116_events_page_loads(self, driver):
        """TC116 – Events page loads successfully."""
        go(driver, "/events.html")
        assert "ZyntraPass" in driver.title or "Event" in driver.title

    def test_TC117_events_heading_visible(self, driver):
        """TC117 – 'Events' heading is visible on the page."""
        go(driver, "/events.html")
        h1 = wait_for(driver, By.TAG_NAME, "h1")
        assert "Events" in h1.text

    def test_TC118_events_subtitle_visible(self, driver):
        """TC118 – Events page subtitle/description is visible."""
        go(driver, "/events.html")
        sub = wait_for(driver, By.CLASS_NAME, "subtitle")
        assert sub.is_displayed()

    def test_TC119_create_event_button_visible(self, driver):
        """TC119 – 'Create event' button is visible on Events page."""
        go(driver, "/events.html")
        btn = wait_for(driver, By.CLASS_NAME, "btn-create")
        assert btn.is_displayed() and "Create" in btn.text

    def test_TC120_create_event_btn_navigates(self, driver):
        """TC120 – Clicking Create Event navigates to create_event.html."""
        go(driver, "/events.html")
        click_when_ready(driver, By.CLASS_NAME, "btn-create")
        WebDriverWait(driver, 10).until(EC.url_contains("create_event"))
        assert "create_event" in driver.current_url

    def test_TC121_search_input_present(self, driver):
        """TC121 – Search input field is present on events page."""
        go(driver, "/events.html")
        search = wait_for(driver, By.ID, "searchInput")
        assert search.is_displayed()

    def test_TC122_search_icon_present(self, driver):
        """TC122 – Search icon is displayed alongside the search bar."""
        go(driver, "/events.html")
        icon = wait_for(driver, By.CLASS_NAME, "search-icon")
        assert icon.is_displayed()

    def test_TC123_search_has_placeholder(self, driver):
        """TC123 – Search input has a placeholder text."""
        go(driver, "/events.html")
        ph = driver.find_element(By.ID, "searchInput").get_attribute("placeholder")
        assert ph and len(ph) > 0

    def test_TC124_search_input_accepts_text(self, driver):
        """TC124 – Search input accepts and retains typed text."""
        go(driver, "/events.html")
        fill(driver, By.ID, "searchInput", "test event")
        val = driver.find_element(By.ID, "searchInput").get_attribute("value")
        assert "test event" == val

    def test_TC125_tabs_section_present(self, driver):
        """TC125 – Tabs section (All, Upcoming, Ongoing, Completed, Cancelled) is present."""
        go(driver, "/events.html")
        tabs = wait_for(driver, By.CLASS_NAME, "tabs")
        assert tabs.is_displayed()

    def test_TC126_tab_all_present(self, driver):
        """TC126 – 'All' tab is present."""
        go(driver, "/events.html")
        tabs = driver.find_elements(By.CLASS_NAME, "tab")
        texts = [t.text for t in tabs]
        assert any("All" in t for t in texts)

    def test_TC127_tab_upcoming_present(self, driver):
        """TC127 – 'Upcoming' tab is present."""
        go(driver, "/events.html")
        tabs = driver.find_elements(By.CLASS_NAME, "tab")
        texts = [t.text for t in tabs]
        assert any("Upcoming" in t for t in texts)

    def test_TC128_tab_ongoing_present(self, driver):
        """TC128 – 'Ongoing' tab is present."""
        go(driver, "/events.html")
        tabs = driver.find_elements(By.CLASS_NAME, "tab")
        texts = [t.text for t in texts]
        assert any("Ongoing" in t for t in texts)

    def test_TC129_tab_completed_present(self, driver):
        """TC129 – 'Completed' tab is present."""
        go(driver, "/events.html")
        tabs = driver.find_elements(By.CLASS_NAME, "tab")
        texts = [t.text for t in tabs]
        assert any("Completed" in t for t in texts)

    def test_TC130_tab_cancelled_present(self, driver):
        """TC130 – 'Cancelled' tab is present."""
        go(driver, "/events.html")
        tabs = driver.find_elements(By.CLASS_NAME, "tab")
        texts = [t.text for t in tabs]
        assert any("Cancelled" in t for t in texts)

    def test_TC131_tab_all_active_by_default(self, driver):
        """TC131 – 'All' tab is the active tab by default."""
        go(driver, "/events.html")
        tabs = driver.find_elements(By.CLASS_NAME, "tab")
        active = [t for t in tabs if "active" in t.get_attribute("class")]
        assert len(active) > 0 and "All" in active[0].text

    def test_TC132_tab_badge_all_visible(self, driver):
        """TC132 – Badge counter for 'All' tab is visible."""
        go(driver, "/events.html")
        badge = wait_for(driver, By.ID, "badge-all")
        assert badge.is_displayed()

    def test_TC133_tab_badge_upcoming_visible(self, driver):
        """TC133 – Badge counter for 'Upcoming' tab is visible."""
        go(driver, "/events.html")
        badge = wait_for(driver, By.ID, "badge-upcoming")
        assert badge.is_displayed()

    def test_TC134_tab_badge_ongoing_visible(self, driver):
        """TC134 – Badge counter for 'Ongoing' tab is visible."""
        go(driver, "/events.html")
        badge = wait_for(driver, By.ID, "badge-ongoing")
        assert badge.is_displayed()

    def test_TC135_tab_badge_completed_visible(self, driver):
        """TC135 – Badge counter for 'Completed' tab is visible."""
        go(driver, "/events.html")
        badge = wait_for(driver, By.ID, "badge-completed")
        assert badge.is_displayed()

    def test_TC136_tab_badge_cancelled_visible(self, driver):
        """TC136 – Badge counter for 'Cancelled' tab is visible."""
        go(driver, "/events.html")
        badge = wait_for(driver, By.ID, "badge-cancelled")
        assert badge.is_displayed()

    def test_TC137_events_feed_container_present(self, driver):
        """TC137 – Events feed container div is present."""
        go(driver, "/events.html")
        feed = wait_for(driver, By.ID, "events-feed")
        assert feed is not None

    def test_TC138_top_bar_visible(self, driver):
        """TC138 – Top bar is visible on events page."""
        go(driver, "/events.html")
        top = wait_for(driver, By.CLASS_NAME, "top-bar")
        assert top.is_displayed()

    def test_TC139_menu_button_visible(self, driver):
        """TC139 – Menu button is visible on events page top bar."""
        go(driver, "/events.html")
        btn = wait_for(driver, By.ID, "menuBtn")
        assert btn.is_displayed()

    def test_TC140_bottom_nav_present(self, driver):
        """TC140 – Bottom navigation is present on events page."""
        go(driver, "/events.html")
        nav = wait_for(driver, By.CLASS_NAME, "bottom-nav")
        assert nav.is_displayed()

    def test_TC141_sidebar_present(self, driver):
        """TC141 – Sidebar is present in DOM on events page."""
        go(driver, "/events.html")
        sidebar = wait_for(driver, By.ID, "sidebar")
        assert sidebar is not None

    def test_TC142_sidebar_opens_on_menu_click(self, driver):
        """TC142 – Menu button opens the sidebar on events page."""
        go(driver, "/events.html")
        click_when_ready(driver, By.ID, "menuBtn")
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#sidebar.active"))
        )

    def test_TC143_upcoming_tab_click_changes_active(self, driver):
        """TC143 – Clicking 'Upcoming' tab makes it the active tab."""
        go(driver, "/events.html")
        tabs = driver.find_elements(By.CLASS_NAME, "tab")
        upcoming = [t for t in tabs if "Upcoming" in t.text]
        if upcoming:
            upcoming[0].click()
            assert "active" in upcoming[0].get_attribute("class")

    def test_TC144_completed_tab_click_changes_active(self, driver):
        """TC144 – Clicking 'Completed' tab makes it the active tab."""
        go(driver, "/events.html")
        tabs = driver.find_elements(By.CLASS_NAME, "tab")
        completed = [t for t in tabs if "Completed" in t.text]
        if completed:
            completed[0].click()
            assert "active" in completed[0].get_attribute("class")

    def test_TC145_cancelled_tab_click_changes_active(self, driver):
        """TC145 – Clicking 'Cancelled' tab makes it the active tab."""
        go(driver, "/events.html")
        tabs = driver.find_elements(By.CLASS_NAME, "tab")
        cancelled = [t for t in tabs if "Cancelled" in t.text]
        if cancelled:
            cancelled[0].click()
            assert "active" in cancelled[0].get_attribute("class")

    def test_TC146_search_container_present(self, driver):
        """TC146 – Search container div is present."""
        go(driver, "/events.html")
        sc = wait_for(driver, By.CLASS_NAME, "search-container")
        assert sc.is_displayed()

    def test_TC147_sidebar_events_link_active(self, driver):
        """TC147 – Sidebar shows 'Events' link as active on events page."""
        go(driver, "/events.html")
        links = driver.find_elements(By.CLASS_NAME, "sidebar-item")
        events_active = [l for l in links if "Events" in l.text and "active" in l.get_attribute("class")]
        assert len(events_active) > 0

    def test_TC148_bottom_nav_events_link_active(self, driver):
        """TC148 – Bottom nav shows Events as the active nav item."""
        go(driver, "/events.html")
        items = driver.find_elements(By.CLASS_NAME, "nav-item")
        events_active = [i for i in items if "Events" in i.text and "active" in i.get_attribute("class")]
        assert len(events_active) > 0

    def test_TC149_supabase_script_loaded(self, driver):
        """TC149 – Supabase CDN script is referenced in the page source."""
        go(driver, "/events.html")
        assert "supabase" in driver.page_source.lower()

    def test_TC150_five_tabs_displayed(self, driver):
        """TC150 – Exactly 5 filter tabs are displayed (All/Upcoming/Ongoing/Completed/Cancelled)."""
        go(driver, "/events.html")
        tabs = driver.find_elements(By.CLASS_NAME, "tab")
        assert len(tabs) == 5
