# =============================================================================
# config.py — Central configuration for ZyntraPass Selenium test suite
# =============================================================================

# ── Deployment URL ────────────────────────────────────────────────────────────
BASE_URL = "https://zyntrapass.vercel.app"   # Update with your Vercel URL

# ── Organizer credentials ─────────────────────────────────────────────────────
ORGANIZER_EMAIL      = "organizer@test.com"
ORGANIZER_PASSWORD   = "Test@1234"
ORGANIZER_SECRET_KEY = "MySecretOrgKey2026"

# ── Attendee credentials ──────────────────────────────────────────────────────
ATTENDEE_EMAIL    = "attendee@test.com"
ATTENDEE_PASSWORD = "Test@1234"

# ── Volunteer code ────────────────────────────────────────────────────────────
VOLUNTEER_CODE = "1234"

# ── Driver settings ───────────────────────────────────────────────────────────
HEADLESS         = True           # Set False to watch tests run
IMPLICIT_WAIT    = 8             # seconds
PAGE_LOAD_TIMEOUT = 30           # seconds
EXPLICIT_WAIT    = 15            # seconds for WebDriverWait

# ── Page paths ────────────────────────────────────────────────────────────────
PAGES = {
    "index":               "/index.html",
    "login":               "/login.html",
    "signup":              "/signup.html",
    "dashboard":           "/dashboard.html",
    "events":              "/events.html",
    "create_event":        "/create_event.html",
    "event_detail":        "/event_detail.html",
    "participants":        "/participants.html",
    "live":                "/live.html",
    "volunteers":          "/volunteers.html",
    "certificates":        "/certificates.html",
    "settings":            "/settings.html",
    "attendee_dashboard":  "/attendee_dashboard.html",
    "attendee_discover":   "/attendee_discover.html",
    "attendee_my_events":  "/attendee_my_events.html",
    "attendee_attendance": "/attendee_attendance.html",
    "attendee_certs":      "/attendee_certificates.html",
    "attendee_settings":   "/attendee_settings.html",
    "attendee_signup":     "/attendee_signup.html",
    "volunteer_dashboard": "/volunteer_dashboard.html",
    "volunteer_scan":      "/volunteer_scan.html",
    "volunteer_participants": "/volunteer_participants.html",
}
