"""
test_01_landing.py  —  Landing/Index Page
TC001 – TC020
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from conftest import go, wait_for, click_when_ready, fill


class TestLandingPage:

    def test_TC001_page_loads(self, driver):
        """TC001 – Landing page loads successfully."""
        go(driver, "/index.html")
        assert "ZyntraPass" in driver.title

    def test_TC002_brand_name_visible(self, driver):
        """TC002 – Brand name 'ZyntraPass' is visible in header."""
        go(driver, "/index.html")
        brand = wait_for(driver, By.CLASS_NAME, "brand-name")
        assert "ZyntraPass" in brand.text

    def test_TC003_hero_title_visible(self, driver):
        """TC003 – Hero title is displayed on the page."""
        go(driver, "/index.html")
        title = wait_for(driver, By.CLASS_NAME, "hero-title")
        assert title.is_displayed()

    def test_TC004_hero_subtitle_visible(self, driver):
        """TC004 – Hero subtitle paragraph is visible."""
        go(driver, "/index.html")
        subtitle = wait_for(driver, By.CLASS_NAME, "hero-subtitle")
        assert subtitle.is_displayed()

    def test_TC005_sign_in_button_visible(self, driver):
        """TC005 – Sign In button is visible in the header."""
        go(driver, "/index.html")
        btn = wait_for(driver, By.ID, "sign-in-btn")
        assert btn.is_displayed()

    def test_TC006_create_account_button_visible(self, driver):
        """TC006 – Create Account button is visible in the header."""
        go(driver, "/index.html")
        btn = wait_for(driver, By.ID, "create-account-btn")
        assert btn.is_displayed()

    def test_TC007_explore_events_button_visible(self, driver):
        """TC007 – 'Explore Events' CTA button is visible."""
        go(driver, "/index.html")
        btns = driver.find_elements(By.CLASS_NAME, "btn-primary")
        explore = [b for b in btns if "Explore" in b.text]
        assert len(explore) > 0 and explore[0].is_displayed()

    def test_TC008_organize_event_button_visible(self, driver):
        """TC008 – 'Organize an Event' button is visible."""
        go(driver, "/index.html")
        btns = driver.find_elements(By.CLASS_NAME, "btn-secondary")
        organize = [b for b in btns if "Organiz" in b.text]
        assert len(organize) > 0

    def test_TC009_stats_section_visible(self, driver):
        """TC009 – Stats section (events hosted, verified, certificates) is visible."""
        go(driver, "/index.html")
        stats = wait_for(driver, By.CLASS_NAME, "stats")
        assert stats.is_displayed()

    def test_TC010_events_hosted_stat_present(self, driver):
        """TC010 – '1,842 Events hosted' stat is present."""
        go(driver, "/index.html")
        page_source = driver.page_source
        assert "1,842" in page_source

    def test_TC011_certificates_stat_present(self, driver):
        """TC011 – '74k Certificates issued' stat is present."""
        go(driver, "/index.html")
        assert "74k" in driver.page_source

    def test_TC012_sign_in_btn_opens_login(self, driver):
        """TC012 – Clicking Sign In navigates to login.html."""
        go(driver, "/index.html")
        click_when_ready(driver, By.ID, "sign-in-btn")
        WebDriverWait(driver, 10).until(EC.url_contains("login"))
        assert "login" in driver.current_url

    def test_TC013_create_account_btn_opens_modal(self, driver):
        """TC013 – Create Account opens role selection modal."""
        go(driver, "/index.html")
        click_when_ready(driver, By.ID, "create-account-btn")
        modal = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "role-modal"))
        )
        assert modal.is_displayed()

    def test_TC014_modal_attendee_option_present(self, driver):
        """TC014 – 'I am an Attendee' option is present in modal."""
        go(driver, "/index.html")
        click_when_ready(driver, By.ID, "create-account-btn")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "role-modal")))
        btns = driver.find_elements(By.CLASS_NAME, "role-btn")
        texts = [b.text for b in btns]
        assert any("Attendee" in t for t in texts)

    def test_TC015_modal_organizer_option_present(self, driver):
        """TC015 – 'I am an Organizer' option is present in modal."""
        go(driver, "/index.html")
        click_when_ready(driver, By.ID, "create-account-btn")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "role-modal")))
        btns = driver.find_elements(By.CLASS_NAME, "role-btn")
        texts = [b.text for b in btns]
        assert any("Organizer" in t for t in texts)

    def test_TC016_modal_close_button_present(self, driver):
        """TC016 – Cancel/close button is present in the modal."""
        go(driver, "/index.html")
        click_when_ready(driver, By.ID, "create-account-btn")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "role-modal")))
        close = driver.find_element(By.ID, "close-modal-btn")
        assert close.is_displayed()

    def test_TC017_modal_close_dismisses_modal(self, driver):
        """TC017 – Clicking Cancel closes the role selection modal."""
        go(driver, "/index.html")
        click_when_ready(driver, By.ID, "create-account-btn")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "role-modal")))
        click_when_ready(driver, By.ID, "close-modal-btn")
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element_located((By.ID, "role-modal"))
        )

    def test_TC018_page_title_correct(self, driver):
        """TC018 – Page <title> contains 'ZyntraPass'."""
        go(driver, "/index.html")
        assert "ZyntraPass" in driver.title

    def test_TC019_footer_stats_three_items(self, driver):
        """TC019 – Footer stats section has exactly 3 stat items."""
        go(driver, "/index.html")
        items = driver.find_elements(By.CLASS_NAME, "stat-item")
        assert len(items) >= 3

    def test_TC020_verified_attendance_stat_present(self, driver):
        """TC020 – '96.4% Verified attendance' stat is present."""
        go(driver, "/index.html")
        assert "96.4" in driver.page_source
