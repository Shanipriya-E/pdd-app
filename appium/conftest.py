"""
conftest.py — Shared Appium fixtures for ZyntraPass mobile test suite.
Sets up and tears down the Appium driver for every test session.
"""

import os
import pytest
from appium import webdriver
from appium.options import UiAutomator2Options


def get_capabilities() -> UiAutomator2Options:
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UIAutomator2"
    options.device_name = os.getenv("DEVICE_NAME", "Android Emulator")
    options.platform_version = os.getenv("ANDROID_VERSION", "13.0")
    options.app = os.getenv("APP_PATH", "./ZyntraPass.apk")
    options.app_package = "com.example.zyntrapass"
    options.app_activity = "com.example.zyntrapass.MainActivity"
    options.no_reset = False
    options.auto_grant_permissions = True
    options.new_command_timeout = 120
    return options


@pytest.fixture(scope="session")
def appium_driver():
    """Session-scoped Appium WebDriver fixture."""
    host = os.getenv("APPIUM_HOST", "127.0.0.1")
    port = os.getenv("APPIUM_PORT", "4723")
    server_url = f"http://{host}:{port}/wd/hub"

    driver = webdriver.Remote(server_url, options=get_capabilities())
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def driver(appium_driver):
    """Function-scoped fixture — resets app state before each test."""
    appium_driver.reset()
    yield appium_driver
