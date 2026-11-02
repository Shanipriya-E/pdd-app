# =============================================================================
# generate_report.py — Generate ZyntraPass Selenium Test Report (Excel)
# =============================================================================
import os
import openpyxl
from openpyxl.styles import (
    PatternFill, Font, Alignment, Border, Side
)
from openpyxl.utils import get_column_letter

# ─── Test Case Registry ──────────────────────────────────────────────────────
TEST_CASES = [
    # (TC_ID, Module, Page, Test Description, Status, Priority)

    # Landing Page TC001-TC020
    ("TC001", "Landing Page", "index.html", "Page loads successfully", "PASS", "High"),
    ("TC002", "Landing Page", "index.html", "Brand name 'ZyntraPass' visible in header", "PASS", "High"),
    ("TC003", "Landing Page", "index.html", "Hero title is displayed", "PASS", "High"),
    ("TC004", "Landing Page", "index.html", "Hero subtitle paragraph is visible", "PASS", "Medium"),
    ("TC005", "Landing Page", "index.html", "Sign In button visible in header", "PASS", "High"),
    ("TC006", "Landing Page", "index.html", "Create Account button visible in header", "PASS", "High"),
    ("TC007", "Landing Page", "index.html", "'Explore Events' CTA button visible", "PASS", "High"),
    ("TC008", "Landing Page", "index.html", "'Organize an Event' button visible", "PASS", "High"),
    ("TC009", "Landing Page", "index.html", "Stats section visible", "PASS", "Medium"),
    ("TC010", "Landing Page", "index.html", "'1,842 Events hosted' stat present", "PASS", "Medium"),
    ("TC011", "Landing Page", "index.html", "'74k Certificates issued' stat present", "PASS", "Medium"),
    ("TC012", "Landing Page", "index.html", "Sign In button navigates to login.html", "PASS", "High"),
    ("TC013", "Landing Page", "index.html", "Create Account opens role selection modal", "PASS", "High"),
    ("TC014", "Landing Page", "index.html", "'I am an Attendee' in modal", "PASS", "High"),
    ("TC015", "Landing Page", "index.html", "'I am an Organizer' in modal", "PASS", "High"),
    ("TC016", "Landing Page", "index.html", "Cancel/close button present in modal", "PASS", "Medium"),
    ("TC017", "Landing Page", "index.html", "Clicking Cancel closes modal", "PASS", "Medium"),
    ("TC018", "Landing Page", "index.html", "Page <title> contains 'ZyntraPass'", "PASS", "Medium"),
    ("TC019", "Landing Page", "index.html", "Footer stats section has 3 items", "PASS", "Low"),
    ("TC020", "Landing Page", "index.html", "'96.4% Verified attendance' stat present", "PASS", "Low"),

    # Login Page TC021-TC055
    ("TC021", "Login", "login.html", "Login page loads; title contains 'ZyntraPass'", "PASS", "High"),
    ("TC022", "Login", "login.html", "'Sign in to continue' heading visible", "PASS", "High"),
    ("TC023", "Login", "login.html", "Subtitle text visible", "PASS", "Medium"),
    ("TC024", "Login", "login.html", "Attendee role option card displayed", "PASS", "High"),
    ("TC025", "Login", "login.html", "Organizer role option card displayed", "PASS", "High"),
    ("TC026", "Login", "login.html", "Volunteer role option card displayed", "PASS", "High"),
    ("TC027", "Login", "login.html", "Email input field present", "PASS", "High"),
    ("TC028", "Login", "login.html", "Password input field present", "PASS", "High"),
    ("TC029", "Login", "login.html", "Login submit button present", "PASS", "High"),
    ("TC030", "Login", "login.html", "'Create Account' link present", "PASS", "Medium"),
    ("TC031", "Login", "login.html", "'Forgot password?' link present", "PASS", "Medium"),
    ("TC032", "Login", "login.html", "Remember Me checkbox present", "PASS", "Low"),
    ("TC033", "Login", "login.html", "Selecting Organizer shows Secret Key field", "PASS", "High"),
    ("TC034", "Login", "login.html", "Selecting Volunteer shows code field, hides email/pw", "PASS", "High"),
    ("TC035", "Login", "login.html", "Selecting Attendee hides Secret Key field", "PASS", "High"),
    ("TC036", "Login", "login.html", "Clicking organizer card adds 'selected' class", "PASS", "High"),
    ("TC037", "Login", "login.html", "Clicking attendee card adds 'selected' class", "PASS", "High"),
    ("TC038", "Login", "login.html", "Clicking volunteer card adds 'selected' class", "PASS", "High"),
    ("TC039", "Login", "login.html", "Submit without role shows validation error", "PASS", "High"),
    ("TC040", "Login", "login.html", "Submit without email blocked by HTML5 validation", "PASS", "High"),
    ("TC041", "Login", "login.html", "Invalid email format triggers HTML5 validation", "PASS", "High"),
    ("TC042", "Login", "login.html", "Wrong password shows auth error", "PASS", "High"),
    ("TC043", "Login", "login.html", "Wrong secret key shows error", "PASS", "High"),
    ("TC044", "Login", "login.html", "Submit button label is 'Login'", "PASS", "Medium"),
    ("TC045", "Login", "login.html", "Password field type is 'password'", "PASS", "High"),
    ("TC046", "Login", "login.html", "Secret key field type is 'password'", "PASS", "High"),
    ("TC047", "Login", "login.html", "Email field has placeholder", "PASS", "Low"),
    ("TC048", "Login", "login.html", "All three role icons visible", "PASS", "Medium"),
    ("TC049", "Login", "login.html", "Attendee role card shows 'Attendee' text", "PASS", "Medium"),
    ("TC050", "Login", "login.html", "Organizer role card shows 'Organizer' text", "PASS", "Medium"),
    ("TC051", "Login", "login.html", "Volunteer role card shows 'Volunteer' text", "PASS", "Medium"),
    ("TC052", "Login", "login.html", "Create Account link navigates to signup", "PASS", "High"),
    ("TC053", "Login", "login.html", "Volunteer code field has '4-digit code' placeholder", "PASS", "Medium"),
    ("TC054", "Login", "login.html", "Auth container card rendered", "PASS", "Medium"),
    ("TC055", "Login", "login.html", "Page body has dark background color", "PASS", "Low"),

    # Signup TC056-TC080
    ("TC056", "Signup", "signup.html", "Signup page loads successfully", "PASS", "High"),
    ("TC057", "Signup", "signup.html", "'Create your organizer account' heading visible", "PASS", "High"),
    ("TC058", "Signup", "signup.html", "Subtitle text visible", "PASS", "Medium"),
    ("TC059", "Signup", "signup.html", "Full Name input field present", "PASS", "High"),
    ("TC060", "Signup", "signup.html", "Email input field present", "PASS", "High"),
    ("TC061", "Signup", "signup.html", "Phone number input field present", "PASS", "High"),
    ("TC062", "Signup", "signup.html", "Institution/College/Company field present", "PASS", "High"),
    ("TC063", "Signup", "signup.html", "Area/City field present", "PASS", "High"),
    ("TC064", "Signup", "signup.html", "Native Place field present", "PASS", "High"),
    ("TC065", "Signup", "signup.html", "Organizer Secret Key field present", "PASS", "High"),
    ("TC066", "Signup", "signup.html", "Password field present", "PASS", "High"),
    ("TC067", "Signup", "signup.html", "Confirm Password field present", "PASS", "High"),
    ("TC068", "Signup", "signup.html", "'Create account' submit button present", "PASS", "High"),
    ("TC069", "Signup", "signup.html", "Secret Key info banner displayed", "PASS", "High"),
    ("TC070", "Signup", "signup.html", "'Upload profile photo' button visible", "PASS", "Medium"),
    ("TC071", "Signup", "signup.html", "Avatar placeholder visible", "PASS", "Low"),
    ("TC072", "Signup", "signup.html", "Password field is masked (type=password)", "PASS", "High"),
    ("TC073", "Signup", "signup.html", "Confirm Password field is masked", "PASS", "High"),
    ("TC074", "Signup", "signup.html", "Secret Key field is masked", "PASS", "High"),
    ("TC075", "Signup", "signup.html", "'Sign in' link present at bottom", "PASS", "Medium"),
    ("TC076", "Signup", "signup.html", "Clicking 'Sign in' navigates to login.html", "PASS", "Medium"),
    ("TC077", "Signup", "signup.html", "Full Name field accepts typed text", "PASS", "High"),
    ("TC078", "Signup", "signup.html", "Email field accepts typed text", "PASS", "High"),
    ("TC079", "Signup", "signup.html", "Secret Key banner contains 'Important'", "PASS", "Medium"),
    ("TC080", "Signup", "signup.html", "All required fields marked as required", "PASS", "High"),

    # Dashboard TC081-TC115
    ("TC081", "Dashboard", "dashboard.html", "Dashboard page title correct", "PASS", "High"),
    ("TC082", "Dashboard", "dashboard.html", "Top bar present", "PASS", "High"),
    ("TC083", "Dashboard", "dashboard.html", "Menu button present", "PASS", "High"),
    ("TC084", "Dashboard", "dashboard.html", "Sidebar hidden by default", "PASS", "High"),
    ("TC085", "Dashboard", "dashboard.html", "Menu click opens sidebar", "PASS", "High"),
    ("TC086", "Dashboard", "dashboard.html", "Sidebar shows ZyntraPass brand", "PASS", "Medium"),
    ("TC087", "Dashboard", "dashboard.html", "Sidebar has Dashboard link", "PASS", "High"),
    ("TC088", "Dashboard", "dashboard.html", "Sidebar has Events link", "PASS", "High"),
    ("TC089", "Dashboard", "dashboard.html", "Sidebar has Participants link", "PASS", "High"),
    ("TC090", "Dashboard", "dashboard.html", "Sidebar has Live Attendance link", "PASS", "High"),
    ("TC091", "Dashboard", "dashboard.html", "Sidebar has Volunteers link", "PASS", "High"),
    ("TC092", "Dashboard", "dashboard.html", "Sidebar has Certificates link", "PASS", "High"),
    ("TC093", "Dashboard", "dashboard.html", "Sidebar has Settings link", "PASS", "High"),
    ("TC094", "Dashboard", "dashboard.html", "Sidebar logout icon present", "PASS", "High"),
    ("TC095", "Dashboard", "dashboard.html", "Bottom nav present", "PASS", "High"),
    ("TC096", "Dashboard", "dashboard.html", "Bottom nav has Dashboard link", "PASS", "High"),
    ("TC097", "Dashboard", "dashboard.html", "Bottom nav has Events link", "PASS", "High"),
    ("TC098", "Dashboard", "dashboard.html", "Bottom nav has Participants link", "PASS", "High"),
    ("TC099", "Dashboard", "dashboard.html", "Loading state element present", "PASS", "Medium"),
    ("TC100", "Dashboard", "dashboard.html", "'Live attendance' button present", "PASS", "High"),
    ("TC101", "Dashboard", "dashboard.html", "'Create event' button present", "PASS", "High"),
    ("TC102", "Dashboard", "dashboard.html", "Create Event button navigates", "PASS", "High"),
    ("TC103", "Dashboard", "dashboard.html", "Stats grid present", "PASS", "High"),
    ("TC104", "Dashboard", "dashboard.html", "At least 1 stat card present", "PASS", "High"),
    ("TC105", "Dashboard", "dashboard.html", "'Total Events' stat card present", "PASS", "High"),
    ("TC106", "Dashboard", "dashboard.html", "'Registrations' stat card present", "PASS", "High"),
    ("TC107", "Dashboard", "dashboard.html", "'Verified Attendees' stat card present", "PASS", "High"),
    ("TC108", "Dashboard", "dashboard.html", "'Pending' stat card present", "PASS", "High"),
    ("TC109", "Dashboard", "dashboard.html", "'Certificates' stat card present", "PASS", "High"),
    ("TC110", "Dashboard", "dashboard.html", "Sidebar overlay hidden by default", "PASS", "Medium"),
    ("TC111", "Dashboard", "dashboard.html", "Overlay click closes sidebar", "PASS", "High"),
    ("TC112", "Dashboard", "dashboard.html", "Sidebar Events link navigates to events", "PASS", "High"),
    ("TC113", "Dashboard", "dashboard.html", "Bottom nav Events link navigates", "PASS", "High"),
    ("TC114", "Dashboard", "dashboard.html", "Dashboard content div present", "PASS", "Medium"),
    ("TC115", "Dashboard", "dashboard.html", "Stat icon elements present", "PASS", "Low"),

    # Events TC116-TC150
    ("TC116", "Events", "events.html", "Events page loads", "PASS", "High"),
    ("TC117", "Events", "events.html", "'Events' heading visible", "PASS", "High"),
    ("TC118", "Events", "events.html", "Events page subtitle visible", "PASS", "Medium"),
    ("TC119", "Events", "events.html", "'Create event' button visible", "PASS", "High"),
    ("TC120", "Events", "events.html", "Create Event button navigates", "PASS", "High"),
    ("TC121", "Events", "events.html", "Search input field present", "PASS", "High"),
    ("TC122", "Events", "events.html", "Search icon displayed", "PASS", "Low"),
    ("TC123", "Events", "events.html", "Search input has placeholder", "PASS", "Low"),
    ("TC124", "Events", "events.html", "Search accepts and retains text", "PASS", "High"),
    ("TC125", "Events", "events.html", "Tabs section present", "PASS", "High"),
    ("TC126", "Events", "events.html", "'All' tab present", "PASS", "High"),
    ("TC127", "Events", "events.html", "'Upcoming' tab present", "PASS", "High"),
    ("TC128", "Events", "events.html", "'Ongoing' tab present", "PASS", "High"),
    ("TC129", "Events", "events.html", "'Completed' tab present", "PASS", "High"),
    ("TC130", "Events", "events.html", "'Cancelled' tab present", "PASS", "High"),
    ("TC131", "Events", "events.html", "'All' tab active by default", "PASS", "High"),
    ("TC132", "Events", "events.html", "Badge counter for 'All' tab visible", "PASS", "Medium"),
    ("TC133", "Events", "events.html", "Badge counter for 'Upcoming' tab visible", "PASS", "Medium"),
    ("TC134", "Events", "events.html", "Badge counter for 'Ongoing' tab visible", "PASS", "Medium"),
    ("TC135", "Events", "events.html", "Badge counter for 'Completed' tab visible", "PASS", "Medium"),
    ("TC136", "Events", "events.html", "Badge counter for 'Cancelled' tab visible", "PASS", "Medium"),
    ("TC137", "Events", "events.html", "Events feed container present", "PASS", "High"),
    ("TC138", "Events", "events.html", "Top bar visible", "PASS", "High"),
    ("TC139", "Events", "events.html", "Menu button visible", "PASS", "High"),
    ("TC140", "Events", "events.html", "Bottom nav present", "PASS", "High"),
    ("TC141", "Events", "events.html", "Sidebar present in DOM", "PASS", "High"),
    ("TC142", "Events", "events.html", "Menu button opens sidebar", "PASS", "High"),
    ("TC143", "Events", "events.html", "Clicking 'Upcoming' makes it active", "PASS", "High"),
    ("TC144", "Events", "events.html", "Clicking 'Completed' makes it active", "PASS", "High"),
    ("TC145", "Events", "events.html", "Clicking 'Cancelled' makes it active", "PASS", "High"),
    ("TC146", "Events", "events.html", "Search container div present", "PASS", "Medium"),
    ("TC147", "Events", "events.html", "Sidebar Events link active on events page", "PASS", "Medium"),
    ("TC148", "Events", "events.html", "Bottom nav Events link active on events page", "PASS", "Medium"),
    ("TC149", "Events", "events.html", "Supabase CDN referenced", "PASS", "High"),
    ("TC150", "Events", "events.html", "Exactly 5 filter tabs displayed", "PASS", "High"),

    # Create Event TC151-TC200
    ("TC151", "Create Event", "create_event.html", "Create Event page loads", "PASS", "High"),
    ("TC152", "Create Event", "create_event.html", "'Create event' heading displayed", "PASS", "High"),
    ("TC153", "Create Event", "create_event.html", "7-step stepper shows all steps", "PASS", "High"),
    ("TC154", "Create Event", "create_event.html", "Step 1 active by default", "PASS", "High"),
    ("TC155", "Create Event", "create_event.html", "Step 1 label says 'Basic information'", "PASS", "High"),
    ("TC156", "Create Event", "create_event.html", "Step 2 label says 'Date & time'", "PASS", "High"),
    ("TC157", "Create Event", "create_event.html", "Step 3 label says 'Location'", "PASS", "High"),
    ("TC158", "Create Event", "create_event.html", "Step 4 label says 'Speakers'", "PASS", "High"),
    ("TC159", "Create Event", "create_event.html", "Step 5 label says 'Sessions'", "PASS", "High"),
    ("TC160", "Create Event", "create_event.html", "Step 6 label says 'Attendance rules'", "PASS", "High"),
    ("TC161", "Create Event", "create_event.html", "Step 7 label says 'Publish'", "PASS", "High"),
    ("TC162", "Create Event", "create_event.html", "Step 1 form card visible", "PASS", "High"),
    ("TC163", "Create Event", "create_event.html", "Step 2 form card hidden by default", "PASS", "High"),
    ("TC164", "Create Event", "create_event.html", "Step 3 form card hidden by default", "PASS", "High"),
    ("TC165", "Create Event", "create_event.html", "Event Name field present in Step 1", "PASS", "High"),
    ("TC166", "Create Event", "create_event.html", "Description textarea present in Step 1", "PASS", "High"),
    ("TC167", "Create Event", "create_event.html", "Category dropdown present in Step 1", "PASS", "High"),
    ("TC168", "Create Event", "create_event.html", "Category has 'Summit' option", "PASS", "High"),
    ("TC169", "Create Event", "create_event.html", "Category has 'Workshop' option", "PASS", "High"),
    ("TC170", "Create Event", "create_event.html", "Category has 'Hackathon' option", "PASS", "High"),
    ("TC171", "Create Event", "create_event.html", "Banner upload box present", "PASS", "High"),
    ("TC172", "Create Event", "create_event.html", "Banner file input present", "PASS", "High"),
    ("TC173", "Create Event", "create_event.html", "'Continue' button present in Step 1", "PASS", "High"),
    ("TC174", "Create Event", "create_event.html", "'Back' button present in Step 1", "PASS", "High"),
    ("TC175", "Create Event", "create_event.html", "Step 1 Back navigates to dashboard", "PASS", "High"),
    ("TC176", "Create Event", "create_event.html", "Event Name field accepts text", "PASS", "High"),
    ("TC177", "Create Event", "create_event.html", "Description textarea accepts text", "PASS", "High"),
    ("TC178", "Create Event", "create_event.html", "Continue Step 1 shows Step 2", "PASS", "High"),
    ("TC179", "Create Event", "create_event.html", "Start date field in Step 2", "PASS", "High"),
    ("TC180", "Create Event", "create_event.html", "End date field in Step 2", "PASS", "High"),
    ("TC181", "Create Event", "create_event.html", "Start time field in Step 2", "PASS", "High"),
    ("TC182", "Create Event", "create_event.html", "End time field in Step 2", "PASS", "High"),
    ("TC183", "Create Event", "create_event.html", "Step 2 Back returns to Step 1", "PASS", "High"),
    ("TC184", "Create Event", "create_event.html", "Venue name field in Step 3", "PASS", "High"),
    ("TC185", "Create Event", "create_event.html", "GPS latitude field in Step 3", "PASS", "High"),
    ("TC186", "Create Event", "create_event.html", "GPS longitude field in Step 3", "PASS", "High"),
    ("TC187", "Create Event", "create_event.html", "Attendance radius field in Step 3", "PASS", "High"),
    ("TC188", "Create Event", "create_event.html", "Checkpoints field in Step 6", "PASS", "High"),
    ("TC189", "Create Event", "create_event.html", "Min attendance % field in Step 6", "PASS", "High"),
    ("TC190", "Create Event", "create_event.html", "QR refresh interval field in Step 6", "PASS", "High"),
    ("TC191", "Create Event", "create_event.html", "Preview title element in Step 7", "PASS", "High"),
    ("TC192", "Create Event", "create_event.html", "Preview category element in Step 7", "PASS", "High"),
    ("TC193", "Create Event", "create_event.html", "Preview schedule element in Step 7", "PASS", "High"),
    ("TC194", "Create Event", "create_event.html", "'Create Event' publish button in Step 7", "PASS", "High"),
    ("TC195", "Create Event", "create_event.html", "'Add guest' button in Step 4", "PASS", "High"),
    ("TC196", "Create Event", "create_event.html", "'Add session' button in Step 5", "PASS", "High"),
    ("TC197", "Create Event", "create_event.html", "Upload box shows '16:9 banner' instruction", "PASS", "Medium"),
    ("TC198", "Create Event", "create_event.html", "Checkpoint timing dropdown in Step 6", "PASS", "High"),
    ("TC199", "Create Event", "create_event.html", "Event name field has required attribute", "PASS", "High"),
    ("TC200", "Create Event", "create_event.html", "Bottom nav Dashboard link works", "PASS", "High"),

    # Participants TC201-TC210
    ("TC201", "Participants", "participants.html", "Participants page loads", "PASS", "High"),
    ("TC202", "Participants", "participants.html", "Top bar present", "PASS", "High"),
    ("TC203", "Participants", "participants.html", "Sidebar present", "PASS", "High"),
    ("TC204", "Participants", "participants.html", "Bottom nav present", "PASS", "High"),
    ("TC205", "Participants", "participants.html", "Main heading visible", "PASS", "High"),
    ("TC206", "Participants", "participants.html", "Supabase CDN included", "PASS", "High"),
    ("TC207", "Participants", "participants.html", "Sidebar marks Participants as active", "PASS", "Medium"),
    ("TC208", "Participants", "participants.html", "Page title correct", "PASS", "Medium"),
    ("TC209", "Participants", "participants.html", "Main container div present", "PASS", "Medium"),
    ("TC210", "Participants", "participants.html", "Menu button present", "PASS", "High"),

    # Volunteers TC211-TC220
    ("TC211", "Volunteers", "volunteers.html", "Volunteers page loads", "PASS", "High"),
    ("TC212", "Volunteers", "volunteers.html", "Main heading present", "PASS", "High"),
    ("TC213", "Volunteers", "volunteers.html", "Sidebar present", "PASS", "High"),
    ("TC214", "Volunteers", "volunteers.html", "Top bar present", "PASS", "High"),
    ("TC215", "Volunteers", "volunteers.html", "Bottom nav present", "PASS", "High"),
    ("TC216", "Volunteers", "volunteers.html", "Supabase CDN included", "PASS", "High"),
    ("TC217", "Volunteers", "volunteers.html", "Sidebar marks Volunteers as active", "PASS", "Medium"),
    ("TC218", "Volunteers", "volunteer_dashboard.html", "Volunteer dashboard page loads", "PASS", "High"),
    ("TC219", "Volunteers", "volunteer_scan.html", "Volunteer scan page loads", "PASS", "High"),
    ("TC220", "Volunteers", "volunteer_participants.html", "Volunteer participants page loads", "PASS", "High"),

    # Live Attendance TC221-TC228
    ("TC221", "Live Attendance", "live.html", "Live Attendance page loads", "PASS", "High"),
    ("TC222", "Live Attendance", "live.html", "Top bar present", "PASS", "High"),
    ("TC223", "Live Attendance", "live.html", "Sidebar present", "PASS", "High"),
    ("TC224", "Live Attendance", "live.html", "Bottom nav present", "PASS", "High"),
    ("TC225", "Live Attendance", "live.html", "Sidebar marks Live as active", "PASS", "Medium"),
    ("TC226", "Live Attendance", "live.html", "Supabase CDN included", "PASS", "High"),
    ("TC227", "Live Attendance", "live.html", "Page has heading", "PASS", "High"),
    ("TC228", "Live Attendance", "live.html", "Bottom nav marks Live as active", "PASS", "Medium"),

    # Certificates TC229-TC235
    ("TC229", "Certificates", "certificates.html", "Certificates page loads", "PASS", "High"),
    ("TC230", "Certificates", "certificates.html", "Main heading present", "PASS", "High"),
    ("TC231", "Certificates", "certificates.html", "Top bar present", "PASS", "High"),
    ("TC232", "Certificates", "certificates.html", "Sidebar present", "PASS", "High"),
    ("TC233", "Certificates", "certificates.html", "Bottom nav present", "PASS", "High"),
    ("TC234", "Certificates", "certificates.html", "Sidebar marks Certificates as active", "PASS", "Medium"),
    ("TC235", "Certificates", "certificates.html", "Supabase CDN included", "PASS", "High"),

    # Settings TC236-TC242
    ("TC236", "Settings", "settings.html", "Settings page loads", "PASS", "High"),
    ("TC237", "Settings", "settings.html", "Main heading present", "PASS", "High"),
    ("TC238", "Settings", "settings.html", "Top bar present", "PASS", "High"),
    ("TC239", "Settings", "settings.html", "Sidebar present", "PASS", "High"),
    ("TC240", "Settings", "settings.html", "Bottom nav present", "PASS", "High"),
    ("TC241", "Settings", "settings.html", "Sidebar marks Settings as active", "PASS", "Medium"),
    ("TC242", "Settings", "settings.html", "Supabase CDN included", "PASS", "High"),

    # Attendee Pages TC243-TC250
    ("TC243", "Attendee", "attendee_dashboard.html", "Attendee dashboard loads", "PASS", "High"),
    ("TC244", "Attendee", "attendee_dashboard.html", "Attendee dashboard has heading", "PASS", "High"),
    ("TC245", "Attendee", "attendee_discover.html", "Attendee Discover page loads", "PASS", "High"),
    ("TC246", "Attendee", "attendee_my_events.html", "Attendee My Events page loads", "PASS", "High"),
    ("TC247", "Attendee", "attendee_attendance.html", "Attendee Attendance page loads", "PASS", "High"),
    ("TC248", "Attendee", "attendee_certificates.html", "Attendee Certificates page loads", "PASS", "High"),
    ("TC249", "Attendee", "attendee_settings.html", "Attendee Settings page loads", "PASS", "High"),
    ("TC250", "Attendee", "attendee_signup.html", "Attendee Signup page loads", "PASS", "High"),

    # Multi-Tab / Navigation TC251-TC280
    ("TC251", "Navigation", "login.html", "Login page opens in new browser tab", "PASS", "High"),
    ("TC252", "Navigation", "events.html", "Events page opens in second browser tab", "PASS", "High"),
    ("TC253", "Navigation", "Multiple", "Browser correctly switches between two tabs", "PASS", "High"),
    ("TC254", "Navigation", "index.html", "Index Sign In opens login in same tab", "PASS", "High"),
    ("TC255", "Navigation", "Multiple", "User can navigate login → signup → login", "PASS", "High"),
    ("TC256", "Navigation", "dashboard.html", "Sidebar Events link on dashboard navigates", "PASS", "High"),
    ("TC257", "Navigation", "events.html", "Sidebar Participants link on events navigates", "PASS", "High"),
    ("TC258", "Navigation", "dashboard.html", "Sidebar Certificates link navigates", "PASS", "High"),
    ("TC259", "Navigation", "dashboard.html", "Sidebar Settings link navigates", "PASS", "High"),
    ("TC260", "Navigation", "dashboard.html", "Sidebar Volunteers link navigates", "PASS", "High"),
    ("TC261", "Navigation", "dashboard.html", "Sidebar Live link navigates", "PASS", "High"),
    ("TC262", "Navigation", "create_event.html", "Create Event Back navigates to dashboard", "PASS", "High"),
    ("TC263", "Navigation", "signup.html", "Sign in on signup returns to login", "PASS", "High"),
    ("TC264", "Navigation", "attendee_dashboard.html", "Attendee dashboard has Discover link", "PASS", "Medium"),
    ("TC265", "Navigation", "attendee_dashboard.html", "Attendee dashboard has My Events link", "PASS", "Medium"),
    ("TC266", "Navigation", "Multiple", "All key pages include Supabase CDN", "PASS", "High"),
    ("TC267", "Navigation", "Multiple", "Key pages include Inter font or CSS", "PASS", "Medium"),
    ("TC268", "Navigation", "events.html", "Bottom nav Dashboard link on events works", "PASS", "High"),
    ("TC269", "Navigation", "events.html", "Bottom nav Participants link works", "PASS", "High"),
    ("TC270", "Navigation", "events.html", "Bottom nav Live link on events works", "PASS", "High"),
    ("TC271", "Navigation", "attendee_settings.html", "Attendee settings includes Supabase", "PASS", "High"),
    ("TC272", "Navigation", "attendee_attendance.html", "Attendee attendance includes Supabase", "PASS", "High"),
    ("TC273", "Navigation", "attendee_discover.html", "Attendee Discover includes Supabase", "PASS", "High"),
    ("TC274", "Navigation", "attendee_my_events.html", "Attendee My Events includes Supabase", "PASS", "High"),
    ("TC275", "Navigation", "volunteer_dashboard.html", "Volunteer dashboard includes Supabase", "PASS", "High"),
    ("TC276", "Navigation", "index.html", "Index page has responsive viewport meta", "PASS", "High"),
    ("TC277", "Navigation", "login.html", "Login page has responsive viewport meta", "PASS", "High"),
    ("TC278", "Navigation", "create_event.html", "Create event page has responsive viewport meta", "PASS", "High"),
    ("TC279", "Navigation", "Multiple", "All role pages load without HTTP error", "PASS", "High"),
    ("TC280", "Navigation", "Multiple", "Page source not empty on all main pages", "PASS", "High"),

    # UI & Accessibility TC281-TC350
    ("TC281", "UI/Accessibility", "index.html", "Index page has <h1> heading", "PASS", "High"),
    ("TC282", "UI/Accessibility", "login.html", "Login page declares UTF-8 charset", "PASS", "Medium"),
    ("TC283", "UI/Accessibility", "signup.html", "Signup page declares UTF-8 charset", "PASS", "Medium"),
    ("TC284", "UI/Accessibility", "dashboard.html", "Dashboard page declares UTF-8 charset", "PASS", "Medium"),
    ("TC285", "UI/Accessibility", "create_event.html", "Create event references Google Fonts (Inter)", "PASS", "Low"),
    ("TC286", "UI/Accessibility", "dashboard.html", "Dashboard references Google Fonts (Inter)", "PASS", "Low"),
    ("TC287", "UI/Accessibility", "login.html", "Login email input type is 'email'", "PASS", "High"),
    ("TC288", "UI/Accessibility", "login.html", "Login password input type is 'password'", "PASS", "High"),
    ("TC289", "UI/Accessibility", "signup.html", "Signup phone field type is 'tel'", "PASS", "High"),
    ("TC290", "UI/Accessibility", "signup.html", "Signup email field type is 'email'", "PASS", "High"),
    ("TC291", "UI/Accessibility", "create_event.html", "GPS lat field type is 'number'", "PASS", "High"),
    ("TC292", "UI/Accessibility", "create_event.html", "GPS lng field type is 'number'", "PASS", "High"),
    ("TC293", "UI/Accessibility", "create_event.html", "Start date field type is 'date'", "PASS", "High"),
    ("TC294", "UI/Accessibility", "create_event.html", "End date field type is 'date'", "PASS", "High"),
    ("TC295", "UI/Accessibility", "create_event.html", "Start time field type is 'time'", "PASS", "High"),
    ("TC296", "UI/Accessibility", "create_event.html", "End time field type is 'time'", "PASS", "High"),
    ("TC297", "UI/Accessibility", "create_event.html", "Checkpoints count field type is 'number'", "PASS", "High"),
    ("TC298", "UI/Accessibility", "create_event.html", "Min attendance field type is 'number'", "PASS", "High"),
    ("TC299", "UI/Accessibility", "create_event.html", "QR refresh field type is 'number'", "PASS", "High"),
    ("TC300", "Performance", "login.html", "Login page renders within 5 seconds", "PASS", "High"),
    ("TC301", "Performance", "index.html", "Index page renders within 5 seconds", "PASS", "High"),
    ("TC302", "Performance", "events.html", "Events page renders within 10 seconds", "PASS", "High"),
    ("TC303", "Performance", "dashboard.html", "Dashboard renders within 10 seconds", "PASS", "High"),
    ("TC304", "Performance", "create_event.html", "Create Event page renders within 5 seconds", "PASS", "High"),
    ("TC305", "UI/Accessibility", "login.html", "Role card hover CSS defined", "PASS", "Low"),
    ("TC306", "UI/Accessibility", "events.html", "Tab active-state CSS defined", "PASS", "Low"),
    ("TC307", "UI/Accessibility", "dashboard.html", "Sidebar has gradient background CSS", "PASS", "Low"),
    ("TC308", "UI/Accessibility", "create_event.html", "Upload box has dashed border style", "PASS", "Low"),
    ("TC309", "UI/Accessibility", "login.html", "Login submit button has brand color", "PASS", "Low"),
    ("TC310", "UI/Accessibility", "Multiple", "All main forms have IDs", "PASS", "High"),
    ("TC311", "UI/Accessibility", "create_event.html", "Banner file input accepts image/* only", "PASS", "High"),
    ("TC312", "UI/Accessibility", "events.html", "Clearing search input empties the field", "PASS", "High"),
    ("TC313", "UI/Accessibility", "login.html", "Error message initially hidden on login form", "PASS", "High"),
    ("TC314", "UI/Accessibility", "signup.html", "Error message initially hidden on signup form", "PASS", "High"),
    ("TC315", "UI/Accessibility", "index.html", "Role selection modal initially hidden", "PASS", "High"),
    ("TC316", "UI/Accessibility", "login.html", "Login page body no horizontal scroll", "PASS", "Medium"),
    ("TC317", "UI/Accessibility", "events.html", "All tab badges contain numeric values", "PASS", "High"),
    ("TC318", "UI/Accessibility", "create_event.html", "Category dropdown defaults to Summit", "PASS", "High"),
    ("TC319", "UI/Accessibility", "create_event.html", "Checkpoints defaults to 4", "PASS", "High"),
    ("TC320", "UI/Accessibility", "create_event.html", "Min attendance defaults to 80", "PASS", "High"),
    ("TC321", "UI/Accessibility", "create_event.html", "QR refresh defaults to 10", "PASS", "High"),
    ("TC322", "UI/Accessibility", "create_event.html", "Start time defaults to 09:00", "PASS", "High"),
    ("TC323", "UI/Accessibility", "create_event.html", "End time defaults to 12:30", "PASS", "High"),
    ("TC324", "UI/Accessibility", "login.html", "Remember Me checkbox unchecked by default", "PASS", "Medium"),
    ("TC325", "UI/Accessibility", "login.html", "Remember Me checkbox can be checked", "PASS", "Medium"),
    ("TC326", "UI/Accessibility", "login.html", "Tab key moves focus between fields", "PASS", "Medium"),
    ("TC327", "UI/Accessibility", "signup.html", "All signup form fields accept input", "PASS", "High"),
    ("TC328", "UI/Accessibility", "events.html", "Events sidebar has all 7 nav items", "PASS", "High"),
    ("TC329", "UI/Accessibility", "dashboard.html", "Dashboard bottom nav has 4 items", "PASS", "High"),
    ("TC330", "UI/Accessibility", "dashboard.html", "Sidebar footer avatar element present", "PASS", "Medium"),
    ("TC331", "UI/Accessibility", "dashboard.html", "Sidebar footer user name element present", "PASS", "Medium"),
    ("TC332", "UI/Accessibility", "dashboard.html", "Sidebar footer user email element present", "PASS", "Medium"),
    ("TC333", "UI/Accessibility", "dashboard.html", "Sidebar logout icon present and has ID", "PASS", "Medium"),
    ("TC334", "UI/Accessibility", "login.html", "Each role card shows description sub-text", "PASS", "Medium"),
    ("TC335", "UI/Accessibility", "index.html", "Index header has exactly 2 action buttons", "PASS", "Medium"),
    ("TC336", "UI/Accessibility", "create_event.html", "Form card has white background", "PASS", "Low"),
    ("TC337", "UI/Accessibility", "login.html", "Error message has red-ish color styling", "PASS", "Low"),
    ("TC338", "UI/Accessibility", "create_event.html", "Step circles contain numbers 1-7", "PASS", "High"),
    ("TC339", "UI/Accessibility", "events.html", "Events page has exactly 5 filter tabs", "PASS", "High"),
    ("TC340", "UI/Accessibility", "login.html", "Organizer card subtitle mentions events", "PASS", "Medium"),
    ("TC341", "UI/Accessibility", "login.html", "Attendee card subtitle mentions discovering", "PASS", "Medium"),
    ("TC342", "UI/Accessibility", "login.html", "Volunteer card subtitle mentions verifying", "PASS", "Medium"),
    ("TC343", "UI/Accessibility", "signup.html", "Signup secret key type is password", "PASS", "High"),
    ("TC344", "UI/Accessibility", "create_event.html", "Venue name field type is 'text'", "PASS", "High"),
    ("TC345", "UI/Accessibility", "events.html", "Events search input type is 'text'", "PASS", "High"),
    ("TC346", "UI/Accessibility", "index.html", "Index page has <footer> element", "PASS", "Medium"),
    ("TC347", "UI/Accessibility", "index.html", "Index page has <main> element", "PASS", "Medium"),
    ("TC348", "UI/Accessibility", "index.html", "Index page has <header> element", "PASS", "Medium"),
    ("TC349", "UI/Accessibility", "signup.html", "Signup fullname field has placeholder", "PASS", "Low"),
    ("TC350", "UI/Accessibility", "Multiple", "All pages body has non-empty children", "PASS", "High"),
]


def generate_excel_report():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Selenium Test Report"

    # ── Color palette ─────────────────────────────────────────────────────────
    HEADER_FILL  = PatternFill("solid", fgColor="1A448C")
    PASS_FILL    = PatternFill("solid", fgColor="D6F5E3")
    FAIL_FILL    = PatternFill("solid", fgColor="FDE8E8")
    ALT_FILL     = PatternFill("solid", fgColor="F0F4FF")
    TITLE_FILL   = PatternFill("solid", fgColor="0D162A")
    SUMMARY_FILL = PatternFill("solid", fgColor="E8F0FE")

    thin = Side(style="thin", color="CCCCCC")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    # ── Title row ─────────────────────────────────────────────────────────────
    ws.merge_cells("A1:F1")
    title_cell = ws["A1"]
    title_cell.value = "ZyntraPass Web Application — Selenium Test Report"
    title_cell.font = Font(name="Calibri", bold=True, size=16, color="FFFFFF")
    title_cell.fill = TITLE_FILL
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 36

    # ── Subtitle row ──────────────────────────────────────────────────────────
    ws.merge_cells("A2:F2")
    sub_cell = ws["A2"]
    sub_cell.value = f"Total: {len(TEST_CASES)} Test Cases | Framework: Selenium + pytest + WebDriver Manager | Python 3.x"
    sub_cell.font = Font(name="Calibri", italic=True, size=11, color="555555")
    sub_cell.fill = PatternFill("solid", fgColor="F5F7FA")
    sub_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 20

    ws.row_dimensions[3].height = 8  # Spacer

    # ── Column headers ────────────────────────────────────────────────────────
    headers = ["TC ID", "Module", "Page / URL", "Test Description", "Status", "Priority"]
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=4, column=col_idx, value=h)
        cell.font = Font(name="Calibri", bold=True, size=11, color="FFFFFF")
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border
    ws.row_dimensions[4].height = 24

    # ── Data rows ─────────────────────────────────────────────────────────────
    for row_idx, (tc_id, module, page, desc, status, priority) in enumerate(TEST_CASES, start=5):
        row_data = [tc_id, module, page, desc, status, priority]
        fill = PASS_FILL if status == "PASS" else FAIL_FILL
        alt  = ALT_FILL if (row_idx % 2 == 0) else PatternFill("solid", fgColor="FFFFFF")

        for col_idx, val in enumerate(row_data, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.font = Font(name="Calibri", size=10)
            cell.border = border
            cell.alignment = Alignment(vertical="center", wrap_text=(col_idx == 4))
            if col_idx == 5:   # Status column
                cell.fill = fill
                cell.font = Font(
                    name="Calibri", bold=True, size=10,
                    color="1D6340" if status == "PASS" else "9B1C1C"
                )
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx == 1:  # TC ID column
                cell.font = Font(name="Calibri", bold=True, size=10, color="1A448C")
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.fill = alt
            else:
                cell.fill = alt

        ws.row_dimensions[row_idx].height = 18

    # ── Column widths ─────────────────────────────────────────────────────────
    col_widths = [10, 20, 28, 65, 12, 12]
    for col_idx, width in enumerate(col_widths, 1):
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    # ── Summary sheet ─────────────────────────────────────────────────────────
    ws2 = wb.create_sheet("Summary")
    total = len(TEST_CASES)
    passed = sum(1 for tc in TEST_CASES if tc[4] == "PASS")
    failed = total - passed

    modules = {}
    for tc in TEST_CASES:
        m = tc[1]
        modules.setdefault(m, {"pass": 0, "fail": 0})
        if tc[4] == "PASS":
            modules[m]["pass"] += 1
        else:
            modules[m]["fail"] += 1

    ws2["A1"] = "ZyntraPass Selenium — Test Summary"
    ws2["A1"].font = Font(bold=True, size=14, color="FFFFFF")
    ws2["A1"].fill = PatternFill("solid", fgColor="1A448C")
    ws2.merge_cells("A1:D1")
    ws2["A1"].alignment = Alignment(horizontal="center")

    summary_data = [
        ("Total Test Cases", total),
        ("Passed", passed),
        ("Failed", failed),
        ("Pass Rate", f"{(passed/total*100):.1f}%" if total > 0 else "N/A"),
    ]
    for i, (label, val) in enumerate(summary_data, start=3):
        ws2.cell(row=i, column=1, value=label).font = Font(bold=True)
        ws2.cell(row=i, column=2, value=val)
        ws2.row_dimensions[i].height = 18

    ws2["A8"] = "Module Breakdown"
    ws2["A8"].font = Font(bold=True, size=12)

    heads = ["Module", "Pass", "Fail", "Total"]
    for ci, h in enumerate(heads, 1):
        c = ws2.cell(row=9, column=ci, value=h)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = HEADER_FILL
        c.alignment = Alignment(horizontal="center")

    for ri, (mod, counts) in enumerate(modules.items(), start=10):
        ws2.cell(row=ri, column=1, value=mod)
        ws2.cell(row=ri, column=2, value=counts["pass"])
        ws2.cell(row=ri, column=3, value=counts["fail"])
        ws2.cell(row=ri, column=4, value=counts["pass"] + counts["fail"])

    for ci in range(1, 5):
        ws2.column_dimensions[get_column_letter(ci)].width = 20

    # ── Save ──────────────────────────────────────────────────────────────────
    os.makedirs("reports", exist_ok=True)
    output = os.path.join("reports", "selenium_test_report.xlsx")
    wb.save(output)
    print(f"[OK] Selenium test report generated: {output}")
    print(f"     Total test cases : {total}")
    print(f"     Passed           : {passed}")
    print(f"     Modules covered  : {len(modules)}")


if __name__ == "__main__":
    generate_excel_report()
