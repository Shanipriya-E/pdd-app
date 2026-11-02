# =============================================================================
# conftest.py — Shared fixtures for ZyntraPass Selenium test suite
# =============================================================================
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from config import (
    BASE_URL, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT, EXPLICIT_WAIT,
    ORGANIZER_EMAIL, ORGANIZER_PASSWORD, ORGANIZER_SECRET_KEY,
    ATTENDEE_EMAIL, ATTENDEE_PASSWORD, VOLUNTEER_CODE
)


def build_driver(headless=True):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,900")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver


@pytest.fixture(scope="session")
def driver():
    """Session-scoped WebDriver — shared across all tests."""
    d = build_driver(headless=True)
    yield d
    d.quit()


@pytest.fixture(scope="function")
def fresh_driver():
    """Function-scoped driver — fresh browser per test."""
    d = build_driver(headless=True)
    yield d
    d.quit()


@pytest.fixture(scope="session")
def wait(driver):
    return WebDriverWait(driver, EXPLICIT_WAIT)


def go(driver, path):
    """Navigate to a page relative to BASE_URL."""
    driver.get(BASE_URL + path)


def wait_for(driver, by, value, timeout=EXPLICIT_WAIT):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def click_when_ready(driver, by, value, timeout=EXPLICIT_WAIT):
    el = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )
    el.click()
    return el


def fill(driver, by, value, text):
    el = wait_for(driver, by, value)
    el.clear()
    el.send_keys(text)
    return el


def login_as_organizer(driver):
    """Helper: full organizer login flow."""
    go(driver, "/login.html")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-role='organizer']"))
    ).click()
    fill(driver, By.ID, "email", ORGANIZER_EMAIL)
    fill(driver, By.ID, "password", ORGANIZER_PASSWORD)
    fill(driver, By.ID, "secretKey", ORGANIZER_SECRET_KEY)
    click_when_ready(driver, By.ID, "submit-btn")


def login_as_attendee(driver):
    """Helper: full attendee login flow."""
    go(driver, "/login.html")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-role='attendee']"))
    ).click()
    fill(driver, By.ID, "email", ATTENDEE_EMAIL)
    fill(driver, By.ID, "password", ATTENDEE_PASSWORD)
    click_when_ready(driver, By.ID, "submit-btn")


def login_as_volunteer(driver):
    """Helper: volunteer login using code."""
    go(driver, "/login.html")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-role='volunteer']"))
    ).click()
    fill(driver, By.ID, "volunteerCode", VOLUNTEER_CODE)
    click_when_ready(driver, By.ID, "submit-btn")
