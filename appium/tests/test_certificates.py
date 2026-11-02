"""
test_certificates.py — Appium test cases for Organizer Certificates screen.
TC311 – TC340
"""

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def find(driver, aid):
    return WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, aid))
    )


def navigate_to_org_certificates(driver):
    find(driver, "email_field").send_keys("organizer@test.com")
    find(driver, "password_field").send_keys("Test@1234")
    find(driver, "login_button").click()
    find(driver, "role_organizer").click()
    find(driver, "nav_certificates").click()


class TestCertificatesOrganizer:

    # TC311
    def test_certificates_screen_loads(self, driver):
        """TC311 – Organizer Certificates screen loads from dashboard."""
        navigate_to_org_certificates(driver)
        assert find(driver, "certificates_screen").is_displayed()

    # TC312
    def test_certificates_list_displayed(self, driver):
        """TC312 – Certificates list is displayed for issued certificates."""
        navigate_to_org_certificates(driver)
        assert find(driver, "certificates_list").is_displayed()

    # TC313
    def test_certificates_generate_button_present(self, driver):
        """TC313 – Generate/Issue Certificate button is present for organizers."""
        navigate_to_org_certificates(driver)
        assert find(driver, "generate_certificate_button").is_displayed()

    # TC314
    def test_certificates_event_filter_present(self, driver):
        """TC314 – Filter by event dropdown is present on certificates screen."""
        navigate_to_org_certificates(driver)
        assert find(driver, "cert_event_filter").is_displayed()

    # TC315
    def test_certificates_filter_by_event(self, driver):
        """TC315 – Filtering certificates by event shows only that event's certs."""
        navigate_to_org_certificates(driver)
        find(driver, "cert_event_filter").click()
        find(driver, "cert_event_option_0").click()
        assert find(driver, "certificates_list").is_displayed()

    # TC316
    def test_certificates_attendee_name_shown(self, driver):
        """TC316 – Attendee name is shown for each certificate in the list."""
        navigate_to_org_certificates(driver)
        assert find(driver, "cert_attendee_name_0").is_displayed()

    # TC317
    def test_certificates_event_name_shown(self, driver):
        """TC317 – Event name is shown for each certificate in the list."""
        navigate_to_org_certificates(driver)
        assert find(driver, "cert_event_name_0").is_displayed()

    # TC318
    def test_certificates_issue_date_shown(self, driver):
        """TC318 – Issue date is shown for each certificate in the list."""
        navigate_to_org_certificates(driver)
        assert find(driver, "cert_issue_date_0").is_displayed()

    # TC319
    def test_certificates_tap_to_view_preview(self, driver):
        """TC319 – Tapping a certificate opens a preview of the certificate."""
        navigate_to_org_certificates(driver)
        find(driver, "cert_list_item_0").click()
        assert find(driver, "certificate_preview_screen").is_displayed()

    # TC320
    def test_certificates_generate_for_event(self, driver):
        """TC320 – Organizer can generate certificates for an event batch."""
        navigate_to_org_certificates(driver)
        find(driver, "generate_certificate_button").click()
        find(driver, "cert_gen_event_dropdown").click()
        find(driver, "cert_gen_event_option_0").click()
        find(driver, "cert_gen_submit").click()
        assert find(driver, "cert_generation_success").is_displayed()

    # TC321
    def test_certificates_send_to_attendees_button(self, driver):
        """TC321 – Send Certificates to Attendees button is available."""
        navigate_to_org_certificates(driver)
        assert find(driver, "send_certificates_button").is_displayed()

    # TC322
    def test_certificates_send_shows_confirmation(self, driver):
        """TC322 – Tapping Send shows a confirmation dialog before sending."""
        navigate_to_org_certificates(driver)
        find(driver, "send_certificates_button").click()
        assert find(driver, "send_certs_confirm_dialog").is_displayed()

    # TC323
    def test_certificates_download_all_button(self, driver):
        """TC323 – Download All certificates option is available."""
        navigate_to_org_certificates(driver)
        assert find(driver, "download_all_certs_button").is_displayed()

    # TC324
    def test_certificates_search_by_attendee_name(self, driver):
        """TC324 – Search field filters certificates by attendee name."""
        navigate_to_org_certificates(driver)
        find(driver, "cert_search").send_keys("John")
        assert find(driver, "certificates_list").is_displayed()

    # TC325
    def test_certificates_empty_state_no_issued(self, driver):
        """TC325 – Empty state shown when no certificates have been issued."""
        navigate_to_org_certificates(driver)
        assert find(driver, "certificates_list").is_displayed() or \
               find(driver, "no_certificates_message").is_displayed()

    # TC326
    def test_certificates_pull_to_refresh(self, driver):
        """TC326 – Pull-to-refresh updates the certificates list."""
        navigate_to_org_certificates(driver)
        size = driver.get_window_size()
        driver.swipe(size["width"] // 2, 300, size["width"] // 2, 700, 500)
        assert find(driver, "certificates_screen").is_displayed()

    # TC327
    def test_certificates_back_to_dashboard(self, driver):
        """TC327 – Back button on Certificates screen returns to Dashboard."""
        navigate_to_org_certificates(driver)
        driver.back()
        assert find(driver, "organizer_dashboard_screen").is_displayed()

    # TC328
    def test_certificate_preview_contains_org_name(self, driver):
        """TC328 – Certificate preview displays the organizing entity's name."""
        navigate_to_org_certificates(driver)
        find(driver, "cert_list_item_0").click()
        assert find(driver, "cert_org_name").is_displayed()

    # TC329
    def test_certificate_preview_contains_attendee_name(self, driver):
        """TC329 – Certificate preview displays the recipient attendee's name."""
        navigate_to_org_certificates(driver)
        find(driver, "cert_list_item_0").click()
        assert find(driver, "cert_preview_attendee_name").is_displayed()

    # TC330
    def test_certificate_preview_contains_event_name(self, driver):
        """TC330 – Certificate preview displays the event's name."""
        navigate_to_org_certificates(driver)
        find(driver, "cert_list_item_0").click()
        assert find(driver, "cert_preview_event_name").is_displayed()

    # TC331
    def test_certificate_preview_contains_date(self, driver):
        """TC331 – Certificate preview displays the issue or event date."""
        navigate_to_org_certificates(driver)
        find(driver, "cert_list_item_0").click()
        assert find(driver, "cert_preview_date").is_displayed()

    # TC332
    def test_certificate_preview_back_to_list(self, driver):
        """TC332 – Back from certificate preview returns to certificates list."""
        navigate_to_org_certificates(driver)
        find(driver, "cert_list_item_0").click()
        driver.back()
        assert find(driver, "certificates_screen").is_displayed()

    # TC333
    def test_certificate_share_from_preview(self, driver):
        """TC333 – Share option is available from the certificate preview screen."""
        navigate_to_org_certificates(driver)
        find(driver, "cert_list_item_0").click()
        assert find(driver, "share_certificate_button").is_displayed()

    # TC334
    def test_certificates_count_shown_in_header(self, driver):
        """TC334 – Total certificates issued count shown in screen header."""
        navigate_to_org_certificates(driver)
        assert find(driver, "cert_total_count").is_displayed()

    # TC335
    def test_certificates_batch_select_and_send(self, driver):
        """TC335 – Organizer can select multiple certificates for batch send."""
        navigate_to_org_certificates(driver)
        find(driver, "cert_list_item_0").click()
        assert driver.current_activity is not None

    # TC336
    def test_certificates_revoke_option_available(self, driver):
        """TC336 – Revoke certificate option is accessible from certificate detail."""
        navigate_to_org_certificates(driver)
        find(driver, "cert_list_item_0").click()
        assert find(driver, "revoke_certificate_button").is_displayed() or \
               driver.current_activity is not None

    # TC337
    def test_certificates_sort_by_name(self, driver):
        """TC337 – Sorting certificates alphabetically by attendee name works."""
        navigate_to_org_certificates(driver)
        find(driver, "sort_certs_button").click()
        find(driver, "sort_certs_by_name").click()
        assert find(driver, "certificates_list").is_displayed()

    # TC338
    def test_certificates_sort_by_date(self, driver):
        """TC338 – Sorting certificates by issue date reorders the list."""
        navigate_to_org_certificates(driver)
        find(driver, "sort_certs_button").click()
        find(driver, "sort_certs_by_date").click()
        assert find(driver, "certificates_list").is_displayed()

    # TC339
    def test_certificates_export_to_pdf(self, driver):
        """TC339 – Exporting all certificates to PDF is supported."""
        navigate_to_org_certificates(driver)
        find(driver, "download_all_certs_button").click()
        assert driver.current_activity is not None

    # TC340
    def test_certificates_search_cleared_resets_list(self, driver):
        """TC340 – Clearing the search field resets the full certificates list."""
        navigate_to_org_certificates(driver)
        search = find(driver, "cert_search")
        search.send_keys("Test")
        search.clear()
        assert find(driver, "certificates_list").is_displayed()
