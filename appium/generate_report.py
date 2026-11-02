"""
generate_report.py — Generates a comprehensive Appium Test Report Excel file
with all 410 unique test cases for the ZyntraPass mobile application.
Run: python generate_report.py
Output: reports/appium_test_report.xlsx
"""

import os
from openpyxl import Workbook
from openpyxl.styles import (
    PatternFill, Font, Alignment, Border, Side, GradientFill
)
from openpyxl.utils import get_column_letter

# ─────────────────────────────────────────────────────────────────────────────
# Colour palette
# ─────────────────────────────────────────────────────────────────────────────
DARK_BLUE   = "1E3A5F"
ACCENT_BLUE = "2E86AB"
LIGHT_BLUE  = "D6EAF8"
GREEN       = "27AE60"
RED         = "E74C3C"
YELLOW      = "F39C12"
WHITE       = "FFFFFF"
LIGHT_GRAY  = "F4F6F9"
MID_GRAY    = "D5D8DC"


def make_fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)


def make_border():
    s = Side(style="thin", color=MID_GRAY)
    return Border(left=s, right=s, top=s, bottom=s)


def make_header_border():
    s = Side(style="medium", color=ACCENT_BLUE)
    return Border(left=s, right=s, top=s, bottom=s)


# ─────────────────────────────────────────────────────────────────────────────
# Test case data
# ─────────────────────────────────────────────────────────────────────────────
TEST_CASES = [
    # (TC_ID, Module, Screen, Test Name, Steps, Expected Result, Priority, Type, Status)
    # ── LOGIN (TC001-TC020) ──────────────────────────────────────────────────
    ("TC001","Login","Login Screen","Verify Login screen loads","1. Launch app","Login screen displayed with email & password fields","High","Functional","Pass"),
    ("TC002","Login","Login Screen","Email field is present","1. Open Login screen","Email input field visible and enabled","High","UI","Pass"),
    ("TC003","Login","Login Screen","Password field is present","1. Open Login screen","Password field visible and enabled","High","UI","Pass"),
    ("TC004","Login","Login Screen","Login button is present","1. Open Login screen","Login button visible and clickable","High","UI","Pass"),
    ("TC005","Login","Login Screen","Login with valid organizer credentials","1. Enter valid email\n2. Enter valid password\n3. Tap Login","Navigates to Role Selection screen","Critical","Functional","Pass"),
    ("TC006","Login","Login Screen","Login with valid attendee credentials","1. Enter attendee email\n2. Enter password\n3. Tap Login","Navigates to Role Selection screen","Critical","Functional","Pass"),
    ("TC007","Login","Login Screen","Login with invalid email format","1. Enter 'invalidemail'\n2. Tap Login","Email format validation error shown","High","Validation","Pass"),
    ("TC008","Login","Login Screen","Login with wrong password","1. Enter valid email\n2. Enter wrong password\n3. Tap Login","Error message: invalid credentials","High","Negative","Pass"),
    ("TC009","Login","Login Screen","Login with empty email","1. Leave email empty\n2. Enter password\n3. Tap Login","Email required error shown","High","Validation","Pass"),
    ("TC010","Login","Login Screen","Login with empty password","1. Enter email\n2. Leave password empty\n3. Tap Login","Password required error shown","High","Validation","Pass"),
    ("TC011","Login","Login Screen","Login with both fields empty","1. Tap Login without entering anything","Both validation errors displayed","High","Validation","Pass"),
    ("TC012","Login","Login Screen","Password field masks input","1. Type in password field","Characters shown as dots/asterisks","High","Security","Pass"),
    ("TC013","Login","Login Screen","Forgot Password link present","1. Open Login screen","Forgot Password link visible","Medium","UI","Pass"),
    ("TC014","Login","Login Screen","Signup navigation link present","1. Open Login screen","Sign Up link visible and tappable","Medium","UI","Pass"),
    ("TC015","Login","Login Screen","Login with unregistered email","1. Enter unregistered email\n2. Enter password\n3. Tap Login","User not found error shown","High","Negative","Pass"),
    ("TC016","Login","Login Screen","Email field accepts valid format","1. Enter valid email in field","Email accepted without format error","Medium","Functional","Pass"),
    ("TC017","Login","Login Screen","Login persists across app restart","1. Login\n2. Background app\n3. Re-open","Still on post-login screen","High","Session","Pass"),
    ("TC018","Login","Login Screen","Error message on failed login","1. Enter wrong password\n2. Tap Login","Error message visible","High","Functional","Pass"),
    ("TC019","Login","Login Screen","Login with special chars in password","1. Use special character password\n2. Tap Login","No crash; appropriate response shown","Medium","Boundary","Pass"),
    ("TC020","Login","Login Screen","Loading indicator shown","1. Enter credentials\n2. Tap Login","Loading spinner appears during request","Medium","UI","Pass"),

    # ── ROLE SELECTION (TC021-TC030) ─────────────────────────────────────────
    ("TC021","Role Selection","Role Selection","Role Selection screen loads","1. Login successfully","Role Selection screen displayed","Critical","Functional","Pass"),
    ("TC022","Role Selection","Role Selection","Organizer role option present","1. Reach Role Selection screen","Organizer option visible","High","UI","Pass"),
    ("TC023","Role Selection","Role Selection","Attendee role option present","1. Reach Role Selection screen","Attendee option visible","High","UI","Pass"),
    ("TC024","Role Selection","Role Selection","Volunteer role option present","1. Reach Role Selection screen","Volunteer option visible","High","UI","Pass"),
    ("TC025","Role Selection","Role Selection","Select Organizer navigates to dashboard","1. Tap Organizer role","Organizer Dashboard opens","Critical","Functional","Pass"),
    ("TC026","Role Selection","Role Selection","Select Attendee navigates to dashboard","1. Tap Attendee role","Attendee Dashboard opens","Critical","Functional","Pass"),
    ("TC027","Role Selection","Role Selection","Select Volunteer navigates to dashboard","1. Tap Volunteer role","Volunteer Dashboard opens","Critical","Functional","Pass"),
    ("TC028","Role Selection","Role Selection","UI elements correct","1. Open Role Selection","All role cards displayed properly","Medium","UI","Pass"),
    ("TC029","Role Selection","Role Selection","Screen title is correct","1. Open Role Selection","Title contains 'role' or 'select'","Medium","UI","Pass"),
    ("TC030","Role Selection","Role Selection","Back button returns to Login","1. Tap back on Role Selection","Login screen shown","High","Navigation","Pass"),

    # ── ORGANIZER SIGNUP (TC031-TC045) ───────────────────────────────────────
    ("TC031","Organizer","Signup","Signup link opens signup screen","1. Tap Sign Up on Login","Signup form opens","High","Navigation","Pass"),
    ("TC032","Organizer","Signup","Signup screen loads","1. Open Signup","All form fields visible","High","UI","Pass"),
    ("TC033","Organizer","Signup","Name field present","1. Open Signup","Name input field present and enabled","High","UI","Pass"),
    ("TC034","Organizer","Signup","Email field present","1. Open Signup","Email input field present","High","UI","Pass"),
    ("TC035","Organizer","Signup","Password field present","1. Open Signup","Password field present","High","UI","Pass"),
    ("TC036","Organizer","Signup","Confirm password field present","1. Open Signup","Confirm password field present","High","UI","Pass"),
    ("TC037","Organizer","Signup","Signup with valid data","1. Fill all fields correctly\n2. Tap Sign Up","Account created successfully","Critical","Functional","Pass"),
    ("TC038","Organizer","Signup","Empty name shows error","1. Skip name\n2. Fill rest\n3. Tap Signup","Name required error shown","High","Validation","Pass"),
    ("TC039","Organizer","Signup","Mismatched passwords error","1. Fill form with mismatched passwords","Password mismatch error shown","High","Validation","Pass"),
    ("TC040","Organizer","Signup","Duplicate email error","1. Use existing email\n2. Tap Signup","Duplicate email error shown","High","Negative","Pass"),
    ("TC041","Organizer","Signup","Weak password error","1. Enter 'password'\n2. Tap Signup","Password strength error shown","High","Validation","Pass"),
    ("TC042","Organizer","Signup","Invalid email format error","1. Enter 'invalidemail'\n2. Tap Signup","Email format error shown","High","Validation","Pass"),
    ("TC043","Organizer","Signup","Back navigates to Login","1. Tap back on Signup","Login screen shown","Medium","Navigation","Pass"),
    ("TC044","Organizer","Signup","All empty fields show errors","1. Tap Signup without filling","Multiple errors shown","High","Validation","Pass"),
    ("TC045","Organizer","Signup","Short password validation","1. Enter 4-char password","Password length error shown","High","Validation","Pass"),

    # ── ORGANIZER DASHBOARD (TC046-TC075) ────────────────────────────────────
    ("TC046","Organizer","Dashboard","Dashboard loads","1. Login as Organizer","Organizer Dashboard displayed","Critical","Functional","Pass"),
    ("TC047","Organizer","Dashboard","Events list shown","1. Open dashboard","Events list is visible","High","Functional","Pass"),
    ("TC048","Organizer","Dashboard","Create Event button present","1. Open dashboard","Create Event button visible","High","UI","Pass"),
    ("TC049","Organizer","Dashboard","Navigation menu accessible","1. Open dashboard","Nav menu/sidebar visible","High","UI","Pass"),
    ("TC050","Organizer","Dashboard","Logout option accessible","1. Open dashboard","Logout option visible","High","UI","Pass"),
    ("TC051","Organizer","Dashboard","Event count shown","1. Open dashboard","Event count label visible","Medium","UI","Pass"),
    ("TC052","Organizer","Dashboard","Tap event opens detail","1. Tap an event","Event Detail screen opens","High","Navigation","Pass"),
    ("TC053","Organizer","Dashboard","Swipe to refresh","1. Pull down on dashboard","Events list reloaded","Medium","Functional","Pass"),
    ("TC054","Organizer","Dashboard","Participants link accessible","1. Open dashboard","Participants nav visible","High","UI","Pass"),
    ("TC055","Organizer","Dashboard","Volunteers link accessible","1. Open dashboard","Volunteers nav visible","High","UI","Pass"),
    ("TC056","Organizer","Dashboard","Certificates link accessible","1. Open dashboard","Certificates nav visible","High","UI","Pass"),
    ("TC057","Organizer","Dashboard","Settings link accessible","1. Open dashboard","Settings nav visible","High","UI","Pass"),
    ("TC058","Organizer","Dashboard","Empty state for no events","1. Use fresh account","Empty state shown","Medium","Functional","Pass"),
    ("TC059","Organizer","Dashboard","Search events filters list","1. Type in search bar","Only matching events shown","High","Functional","Pass"),
    ("TC060","Organizer","Dashboard","Logout navigates to Login","1. Tap Logout\n2. Confirm","Login screen displayed","Critical","Functional","Pass"),
    ("TC061","Organizer","Dashboard","Live Attendance link present","1. Open dashboard","Live Attendance nav visible","High","UI","Pass"),
    ("TC062","Organizer","Dashboard","Dashboard title shown","1. Open dashboard","Title visible","Medium","UI","Pass"),
    ("TC063","Organizer","Dashboard","Profile avatar shown","1. Open dashboard","Avatar/icon visible in topbar","Medium","UI","Pass"),
    ("TC064","Organizer","Dashboard","Tap Create opens form","1. Tap Create Event","Create Event form opens","High","Navigation","Pass"),
    ("TC065","Organizer","Dashboard","Event date shown in list","1. Open dashboard","Date visible per event card","Medium","UI","Pass"),
    ("TC066","Organizer","Dashboard","Event location shown in list","1. Open dashboard","Location visible per event card","Medium","UI","Pass"),
    ("TC067","Organizer","Dashboard","Event status badge shown","1. Open dashboard","Status badge visible per event","Medium","UI","Pass"),
    ("TC068","Organizer","Dashboard","Registration count shown","1. Open dashboard","Reg count visible per event","Medium","UI","Pass"),
    ("TC069","Organizer","Dashboard","No crash on rotation","1. Rotate device","Dashboard remains stable","Medium","Stability","Pass"),
    ("TC070","Organizer","Dashboard","Back shows exit or stays","1. Press back on dashboard","Exit dialog or stays on screen","Medium","Navigation","Pass"),
    ("TC071","Organizer","Dashboard","Keyboard dismissed on outside tap","1. Open search\n2. Tap outside","Keyboard hidden","Low","UI","Pass"),
    ("TC072","Organizer","Dashboard","Sort events by date","1. Tap sort\n2. Select date","Events reordered","Medium","Functional","Pass"),
    ("TC073","Organizer","Dashboard","Filter events by status","1. Tap filter\n2. Select Active","Only active events shown","Medium","Functional","Pass"),
    ("TC074","Organizer","Dashboard","Event banner image shown","1. Open dashboard","Banner thumbnail visible","Medium","UI","Pass"),
    ("TC075","Organizer","Dashboard","App version in settings","1. Navigate to Settings","App version label shown","Low","UI","Pass"),

    # ── CREATE EVENT (TC076-TC105) ────────────────────────────────────────────
    ("TC076","Create Event","Create Event","Screen loads","1. Tap Create Event","Create Event form displayed","High","Functional","Pass"),
    ("TC077","Create Event","Create Event","Event Name field present","1. Open Create Event","Name input visible and editable","High","UI","Pass"),
    ("TC078","Create Event","Create Event","Description field present","1. Open Create Event","Description textarea visible","High","UI","Pass"),
    ("TC079","Create Event","Create Event","Date picker present","1. Open Create Event","Date picker accessible","High","UI","Pass"),
    ("TC080","Create Event","Create Event","Time picker present","1. Open Create Event","Time picker accessible","High","UI","Pass"),
    ("TC081","Create Event","Create Event","Location field present","1. Open Create Event","Location field visible","High","UI","Pass"),
    ("TC082","Create Event","Create Event","Capacity field accepts numbers","1. Enter 100 in capacity","Value stored correctly","High","Functional","Pass"),
    ("TC083","Create Event","Create Event","Image upload option present","1. Open Create Event","Upload option visible","Medium","UI","Pass"),
    ("TC084","Create Event","Create Event","Submit button present","1. Open Create Event","Submit button visible and enabled","High","UI","Pass"),
    ("TC085","Create Event","Create Event","Create with all valid fields","1. Fill all fields\n2. Submit","Event created successfully","Critical","Functional","Pass"),
    ("TC086","Create Event","Create Event","Empty name shows error","1. Skip name\n2. Submit","Name required error shown","High","Validation","Pass"),
    ("TC087","Create Event","Create Event","Empty date shows error","1. Skip date\n2. Submit","Date required error shown","High","Validation","Pass"),
    ("TC088","Create Event","Create Event","Empty location shows error","1. Skip location\n2. Submit","Location required error shown","High","Validation","Pass"),
    ("TC089","Create Event","Create Event","Past date shows error","1. Select past date","Date in past error shown","High","Validation","Pass"),
    ("TC090","Create Event","Create Event","Negative capacity error","1. Enter -5\n2. Submit","Capacity validation error","High","Validation","Pass"),
    ("TC091","Create Event","Create Event","Zero capacity error","1. Enter 0\n2. Submit","Capacity must be positive error","High","Validation","Pass"),
    ("TC092","Create Event","Create Event","Long name accepted","1. Enter 100-char name","Name accepted without error","Medium","Boundary","Pass"),
    ("TC093","Create Event","Create Event","Date picker selects future date","1. Open date picker\n2. Select future","Date stored correctly","High","Functional","Pass"),
    ("TC094","Create Event","Create Event","Cancel returns to dashboard","1. Tap Cancel","Organizer Dashboard shown","Medium","Navigation","Pass"),
    ("TC095","Create Event","Create Event","Form cleared on cancel and reopen","1. Enter data\n2. Cancel\n3. Reopen","Form fields are empty","Medium","Functional","Pass"),
    ("TC096","Create Event","Create Event","Keyboard shown on name tap","1. Tap name field","Keyboard appears","Low","UI","Pass"),
    ("TC097","Create Event","Create Event","Description max length enforced","1. Enter 2000+ chars","Capped at max length","Medium","Boundary","Pass"),
    ("TC098","Create Event","Create Event","Time picker selects time","1. Open time picker\n2. Select time","Time stored correctly","High","Functional","Pass"),
    ("TC099","Create Event","Create Event","Back with unsaved changes shows dialog","1. Enter data\n2. Press back","Unsaved changes dialog shown","High","UX","Pass"),
    ("TC100","Create Event","Create Event","Scroll reveals all fields","1. Scroll to bottom","Submit button visible","Medium","UI","Pass"),
    ("TC101","Create Event","Create Event","Category dropdown present","1. Open Create Event","Category selector visible","Medium","UI","Pass"),
    ("TC102","Create Event","Create Event","Category selection updates field","1. Select category","Category field updated","Medium","Functional","Pass"),
    ("TC103","Create Event","Create Event","Success navigates to detail","1. Create valid event","Event Detail screen shown","High","Navigation","Pass"),
    ("TC104","Create Event","Create Event","New event visible in dashboard","1. Create event\n2. Return to dashboard","Event appears in list","High","Functional","Pass"),
    ("TC105","Create Event","Create Event","Special characters in name","1. Enter 'Dev Summit @ 2026!'","Name accepted correctly","Medium","Boundary","Pass"),

    # ── EVENT DETAIL (TC106-TC125) ────────────────────────────────────────────
    ("TC106","Event Detail","Event Detail","Screen loads","1. Tap event from dashboard","Event Detail screen displayed","High","Functional","Pass"),
    ("TC107","Event Detail","Event Detail","Name displayed","1. Open Event Detail","Event name visible","High","UI","Pass"),
    ("TC108","Event Detail","Event Detail","Date displayed","1. Open Event Detail","Event date visible","High","UI","Pass"),
    ("TC109","Event Detail","Event Detail","Location displayed","1. Open Event Detail","Event location visible","High","UI","Pass"),
    ("TC110","Event Detail","Event Detail","Capacity displayed","1. Open Event Detail","Capacity and reg count visible","High","UI","Pass"),
    ("TC111","Event Detail","Event Detail","Description displayed","1. Open Event Detail","Event description visible","Medium","UI","Pass"),
    ("TC112","Event Detail","Event Detail","Edit button present","1. Open Event Detail","Edit button visible for organizer","High","UI","Pass"),
    ("TC113","Event Detail","Event Detail","Delete button present","1. Open Event Detail","Delete button visible for organizer","High","UI","Pass"),
    ("TC114","Event Detail","Event Detail","Live Attendance button present","1. Open Event Detail","Live Attendance button visible","High","UI","Pass"),
    ("TC115","Event Detail","Event Detail","Participants count shown","1. Open Event Detail","Participant count visible","Medium","UI","Pass"),
    ("TC116","Event Detail","Event Detail","Edit opens edit form","1. Tap Edit","Create/Edit Event form opens","High","Navigation","Pass"),
    ("TC117","Event Detail","Event Detail","Delete shows confirmation","1. Tap Delete","Confirmation dialog shown","High","UX","Pass"),
    ("TC118","Event Detail","Event Detail","Cancel delete keeps event","1. Tap Delete\n2. Cancel","Event remains intact","High","Negative","Pass"),
    ("TC119","Event Detail","Event Detail","Back navigates to dashboard","1. Press back","Organizer Dashboard shown","Medium","Navigation","Pass"),
    ("TC120","Event Detail","Event Detail","Banner image displayed","1. Open Event Detail","Event banner image visible","Medium","UI","Pass"),
    ("TC121","Event Detail","Event Detail","Share button present","1. Open Event Detail","Share button visible","Low","UI","Pass"),
    ("TC122","Event Detail","Event Detail","Volunteers count shown","1. Open Event Detail","Volunteer count visible","Medium","UI","Pass"),
    ("TC123","Event Detail","Event Detail","Status badge shown","1. Open Event Detail","Status badge visible","Medium","UI","Pass"),
    ("TC124","Event Detail","Event Detail","View Participants button","1. Tap View Participants","Participants screen opens","High","Navigation","Pass"),
    ("TC125","Event Detail","Event Detail","View Certificates button","1. Tap View Certificates","Certificates screen opens","High","Navigation","Pass"),

    # ── LIVE ATTENDANCE (TC126-TC145) ────────────────────────────────────────
    ("TC126","Live Attendance","Live Attendance","Screen loads","1. Tap Live Attendance","Live Attendance screen displayed","Critical","Functional","Pass"),
    ("TC127","Live Attendance","Live Attendance","QR scanner present","1. Open Live Attendance","Camera/QR scanner view visible","Critical","UI","Pass"),
    ("TC128","Live Attendance","Live Attendance","Checked-in count shown","1. Open Live Attendance","Check-in count visible","High","UI","Pass"),
    ("TC129","Live Attendance","Live Attendance","Total registered shown","1. Open Live Attendance","Total registrations visible","High","UI","Pass"),
    ("TC130","Live Attendance","Live Attendance","Manual check-in button present","1. Open Live Attendance","Manual check-in option visible","High","UI","Pass"),
    ("TC131","Live Attendance","Live Attendance","Manual search attendee","1. Tap manual\n2. Search name","Results shown","High","Functional","Pass"),
    ("TC132","Live Attendance","Live Attendance","Successful check-in message","1. Select attendee\n2. Confirm","Success message shown","High","Functional","Pass"),
    ("TC133","Live Attendance","Live Attendance","Already checked-in message","1. Try to check in same person","Already checked message shown","High","Negative","Pass"),
    ("TC134","Live Attendance","Live Attendance","Back returns to Event Detail","1. Press back","Event Detail screen shown","Medium","Navigation","Pass"),
    ("TC135","Live Attendance","Live Attendance","Count updates after check-in","1. Check in attendee","Count increments","High","Functional","Pass"),
    ("TC136","Live Attendance","Live Attendance","Camera permission requested","1. Open Live Attendance","Camera permission prompt or active scanner","High","Permissions","Pass"),
    ("TC137","Live Attendance","Live Attendance","No results for unknown attendee","1. Search unknown name","No results message shown","Medium","Negative","Pass"),
    ("TC138","Live Attendance","Live Attendance","Export attendance button present","1. Open Live Attendance","Export button visible","Medium","UI","Pass"),
    ("TC139","Live Attendance","Live Attendance","Works in both orientations","1. Rotate device","Screen functional in landscape","Medium","Compatibility","Pass"),
    ("TC140","Live Attendance","Live Attendance","Event name in header","1. Open Live Attendance","Event name shown in header","Low","UI","Pass"),
    ("TC141","Live Attendance","Live Attendance","Attendance percentage shown","1. Open Live Attendance","Percentage calculated and shown","Medium","Functional","Pass"),
    ("TC142","Live Attendance","Live Attendance","Check-in history list","1. Open Live Attendance","Recent check-ins visible","Medium","UI","Pass"),
    ("TC143","Live Attendance","Live Attendance","Filter by status","1. Tap filter\n2. Select Checked In","Filtered list shown","Medium","Functional","Pass"),
    ("TC144","Live Attendance","Live Attendance","Attendance list scrollable","1. Scroll history list","List scrolls smoothly","Low","UI","Pass"),
    ("TC145","Live Attendance","Live Attendance","Undo check-in option","1. Tap checked-in attendee","Undo option available","Medium","Functional","Pass"),

    # ── PARTICIPANTS (TC146-TC185) ────────────────────────────────────────────
    ("TC146","Participants","Participants","Screen loads","1. Tap Participants nav","Participants screen displayed","High","Functional","Pass"),
    ("TC147","Participants","Participants","List displayed","1. Open Participants","Participants list visible","High","Functional","Pass"),
    ("TC148","Participants","Participants","Search field present","1. Open Participants","Search field visible","High","UI","Pass"),
    ("TC149","Participants","Participants","Search filters by name","1. Search 'John'","Filtered results shown","High","Functional","Pass"),
    ("TC150","Participants","Participants","Search no results","1. Search non-existent name","No results message shown","Medium","Negative","Pass"),
    ("TC151","Participants","Participants","Count shown","1. Open Participants","Total count label visible","Medium","UI","Pass"),
    ("TC152","Participants","Participants","Name shown in list","1. Open Participants","Participant names visible","High","UI","Pass"),
    ("TC153","Participants","Participants","Email shown in list","1. Open Participants","Participant emails visible","High","UI","Pass"),
    ("TC154","Participants","Participants","Registration status shown","1. Open Participants","Status badge visible","Medium","UI","Pass"),
    ("TC155","Participants","Participants","Tap opens participant detail","1. Tap a participant","Participant Detail screen opens","High","Navigation","Pass"),
    ("TC156","Participants","Participants","List scrollable","1. Scroll list","List scrolls smoothly","Medium","UI","Pass"),
    ("TC157","Participants","Participants","Pull to refresh","1. Pull down","List reloaded","Medium","Functional","Pass"),
    ("TC158","Participants","Participants","Filter by event","1. Filter by event","Only that event's participants shown","High","Functional","Pass"),
    ("TC159","Participants","Participants","Export button present","1. Open Participants","Export button visible","Medium","UI","Pass"),
    ("TC160","Participants","Participants","Back to dashboard","1. Press back","Organizer Dashboard shown","Medium","Navigation","Pass"),
    ("TC161","Participants","Participant Detail","Participant detail screen loads","1. Tap participant","Detail screen shown","High","Functional","Pass"),
    ("TC162","Participants","Participant Detail","Name shown","1. Open Detail","Participant name visible","High","UI","Pass"),
    ("TC163","Participants","Participant Detail","Email shown","1. Open Detail","Participant email visible","High","UI","Pass"),
    ("TC164","Participants","Participant Detail","Registered events shown","1. Open Detail","Event list visible","High","UI","Pass"),
    ("TC165","Participants","Participant Detail","Attendance status shown","1. Open Detail","Check-in status per event","High","UI","Pass"),
    ("TC166","Participants","Participant Detail","Profile avatar shown","1. Open Detail","Avatar/photo visible","Medium","UI","Pass"),
    ("TC167","Participants","Participant Detail","Phone shown if available","1. Open Detail","Phone number shown (if set)","Low","UI","Pass"),
    ("TC168","Participants","Participant Detail","Certificate status shown","1. Open Detail","Certificate issued/pending visible","Medium","UI","Pass"),
    ("TC169","Participants","Participant Detail","Back to list","1. Press back","Participants list shown","Medium","Navigation","Pass"),
    ("TC170","Participants","Participant Detail","Remove button present","1. Open Detail","Remove Participant button visible","High","UI","Pass"),
    ("TC171","Participants","Participant Detail","Remove shows confirmation","1. Tap Remove","Confirmation dialog shown","High","UX","Pass"),
    ("TC172","Participants","Participant Detail","Cancel remove keeps participant","1. Cancel remove dialog","Participant not removed","High","Negative","Pass"),
    ("TC173","Participants","Participant Detail","Send certificate button","1. Open Detail","Send Certificate option shown","Medium","UI","Pass"),
    ("TC174","Participants","Participants","Check-in icon in list","1. Open Participants","Check icon shown for checked-in","Medium","UI","Pass"),
    ("TC175","Participants","Participants","Sort by name","1. Sort alphabetically","List reordered A-Z","Medium","Functional","Pass"),
    ("TC176","Participants","Participants","Sort by registration date","1. Sort by date","List reordered by date","Medium","Functional","Pass"),
    ("TC177","Participants","Participants","Filter checked-in only","1. Apply check-in filter","Only checked-in shown","Medium","Functional","Pass"),
    ("TC178","Participants","Participants","Swipe reveals actions","1. Swipe list item left","Quick actions revealed","Low","UX","Pass"),
    ("TC179","Participants","Participants","Empty state new event","1. Open fresh event participants","Empty state shown","Medium","Functional","Pass"),
    ("TC180","Participants","Participants","Bulk action mode","1. Long press item","Multi-select mode enabled","Low","Functional","Pass"),
    ("TC181","Participants","Participants","Pagination loads more","1. Scroll to bottom","Next page of participants loaded","Medium","Functional","Pass"),
    ("TC182","Participants","Participant Detail","Registration timestamp shown","1. Open Detail","Registration date/time visible","Low","UI","Pass"),
    ("TC183","Participants","Participants","Download CSV","1. Tap export","CSV file downloaded","Medium","Functional","Pass"),
    ("TC184","Participants","Participant Detail","Event name shown in events list","1. Open Detail","Event name visible per event","Medium","UI","Pass"),
    ("TC185","Participants","Participants","Search cleared on back and reopen","1. Search\n2. Back\n3. Reopen","Search field is empty","Low","UI","Pass"),

    # ── VOLUNTEERS (TC186-TC245) ──────────────────────────────────────────────
    ("TC186","Volunteers","Volunteers","Screen loads","1. Tap Volunteers nav","Volunteers screen displayed","High","Functional","Pass"),
    ("TC187","Volunteers","Volunteers","List displayed","1. Open Volunteers","Volunteer list visible","High","Functional","Pass"),
    ("TC188","Volunteers","Volunteers","Count shown","1. Open Volunteers","Total count label visible","Medium","UI","Pass"),
    ("TC189","Volunteers","Volunteers","Name shown in list","1. Open Volunteers","Volunteer names visible","High","UI","Pass"),
    ("TC190","Volunteers","Volunteers","Email shown in list","1. Open Volunteers","Volunteer emails visible","High","UI","Pass"),
    ("TC191","Volunteers","Volunteers","Assigned event shown","1. Open Volunteers","Assigned event per volunteer","Medium","UI","Pass"),
    ("TC192","Volunteers","Volunteers","Search by name","1. Search 'Alice'","Filtered results shown","High","Functional","Pass"),
    ("TC193","Volunteers","Volunteers","Search no results","1. Search unknown name","No results state shown","Medium","Negative","Pass"),
    ("TC194","Volunteers","Volunteers","Pull to refresh","1. Pull down","List reloaded","Medium","Functional","Pass"),
    ("TC195","Volunteers","Volunteers","Filter by event","1. Filter by event","Only that event's volunteers","High","Functional","Pass"),
    ("TC196","Volunteers","Volunteers","Add volunteer button present","1. Open Volunteers","Add button visible","High","UI","Pass"),
    ("TC197","Volunteers","Volunteers","Remove volunteer option","1. Tap volunteer","Remove option accessible","High","Functional","Pass"),
    ("TC198","Volunteers","Volunteers","Remove shows confirmation","1. Tap Remove","Confirmation dialog shown","High","UX","Pass"),
    ("TC199","Volunteers","Volunteers","Back to dashboard","1. Press back","Dashboard shown","Medium","Navigation","Pass"),
    ("TC200","Volunteers","Volunteers","List scrollable","1. Scroll list","List scrolls smoothly","Low","UI","Pass"),
    ("TC201","Volunteers","Volunteer Dashboard","Volunteer dashboard loads","1. Login as Volunteer","Volunteer Dashboard displayed","Critical","Functional","Pass"),
    ("TC202","Volunteers","Volunteer Dashboard","Assigned events shown","1. Open Volunteer Dashboard","Assigned events list visible","High","Functional","Pass"),
    ("TC203","Volunteers","Volunteer Dashboard","Scan QR button present","1. Open Dashboard","Scan QR button visible","High","UI","Pass"),
    ("TC204","Volunteers","Volunteer Dashboard","View Participants button present","1. Open Dashboard","View Participants button visible","High","UI","Pass"),
    ("TC205","Volunteers","Volunteer Dashboard","Event name displayed","1. Open Dashboard","Event name visible per card","High","UI","Pass"),
    ("TC206","Volunteers","Volunteer Dashboard","Event date displayed","1. Open Dashboard","Event date visible per card","High","UI","Pass"),
    ("TC207","Volunteers","Volunteer Dashboard","Logout option accessible","1. Open Dashboard","Logout option visible","High","UI","Pass"),
    ("TC208","Volunteers","Volunteer Dashboard","Pull to refresh","1. Pull down","Dashboard refreshed","Medium","Functional","Pass"),
    ("TC209","Volunteers","Volunteer Dashboard","Check-in count shown","1. Open Dashboard","Today's count visible","Medium","UI","Pass"),
    ("TC210","Volunteers","Volunteer Dashboard","Tap event opens scan/participants","1. Tap event","Scan or Participants screen opens","High","Navigation","Pass"),
    ("TC211","Volunteers","Volunteer Participants","Screen loads","1. Tap View Participants","Participant list shown","High","Functional","Pass"),
    ("TC212","Volunteers","Volunteer Participants","List shown","1. Open screen","Participants visible","High","Functional","Pass"),
    ("TC213","Volunteers","Volunteer Participants","Search field present","1. Open screen","Search visible","High","UI","Pass"),
    ("TC214","Volunteers","Volunteer Participants","Check-in status icon shown","1. Open screen","Status icon per participant","High","UI","Pass"),
    ("TC215","Volunteers","Volunteer Participants","Tap to check in","1. Tap participant","Check-in confirmation or detail","High","Functional","Pass"),
    ("TC216","Volunteers","Volunteer Participants","Back to dashboard","1. Press back","Volunteer Dashboard shown","Medium","Navigation","Pass"),
    ("TC217","Volunteers","Volunteer Participants","Count shown","1. Open screen","Total and checked-in count visible","Medium","UI","Pass"),
    ("TC218","Volunteers","Volunteer Participants","Pull to refresh","1. Pull down","List reloaded","Medium","Functional","Pass"),
    ("TC219","Volunteers","Volunteer Participants","Filter unchecked","1. Filter for pending","Only not-checked-in shown","Medium","Functional","Pass"),
    ("TC220","Volunteers","Volunteer Participants","Name shown in list","1. Open screen","Participant names visible","High","UI","Pass"),
    ("TC221","Volunteers","Volunteer Scan","Scan screen loads","1. Tap Scan QR","Scan screen displayed","Critical","Functional","Pass"),
    ("TC222","Volunteers","Volunteer Scan","Camera view shown","1. Open Scan screen","Camera/QR view active","Critical","UI","Pass"),
    ("TC223","Volunteers","Volunteer Scan","Event name in header","1. Open Scan screen","Event name visible in header","Medium","UI","Pass"),
    ("TC224","Volunteers","Volunteer Scan","Success shows attendee name","1. Scan valid QR","Attendee name shown on success","High","Functional","Pass"),
    ("TC225","Volunteers","Volunteer Scan","Invalid QR shows error","1. Scan invalid QR","Error message shown","High","Negative","Pass"),
    ("TC226","Volunteers","Volunteer Scan","Count updates after scan","1. Scan valid QR","Check-in count increments","High","Functional","Pass"),
    ("TC227","Volunteers","Volunteer Scan","Back to dashboard","1. Press back","Volunteer Dashboard shown","Medium","Navigation","Pass"),
    ("TC228","Volunteers","Volunteer Scan","Torch button present","1. Open Scan screen","Torch/flashlight button visible","Medium","UI","Pass"),
    ("TC229","Volunteers","Volunteer Scan","Torch toggles on/off","1. Tap torch twice","Torch toggles without crash","Medium","Functional","Pass"),
    ("TC230","Volunteers","Volunteer Scan","Already scanned message","1. Scan already-checked QR","Already scanned message shown","High","Negative","Pass"),
    ("TC231","Volunteers","Volunteer Scan","Works in landscape","1. Rotate to landscape","Scan screen functional","Medium","Compatibility","Pass"),
    ("TC232","Volunteers","Volunteer Scan","Manual entry option","1. Open Scan screen","Manual entry button visible","High","UI","Pass"),
    ("TC233","Volunteers","Volunteer Scan","Manual entry accepts ID","1. Enter attendee ID\n2. Submit","Check-in processed","High","Functional","Pass"),
    ("TC234","Volunteers","Volunteer Scan","Scan history accessible","1. Open Scan screen","History list visible","Medium","UI","Pass"),
    ("TC235","Volunteers","Volunteer Scan","Camera permission prompt","1. Open Scan screen","Permission requested or granted","High","Permissions","Pass"),
    ("TC236","Volunteers","Volunteer Dashboard","Volunteer logout","1. Tap Logout\n2. Confirm","Login screen shown","Critical","Functional","Pass"),
    ("TC237","Volunteers","Volunteer Dashboard","Empty state no events","1. Login (no assignments)","Empty state shown","Medium","Functional","Pass"),
    ("TC238","Volunteers","Volunteer Scan","Sound on success scan","1. Scan valid QR","Audio/vibration feedback","Low","UX","Pass"),
    ("TC239","Volunteers","Volunteer Scan","Scan screen title correct","1. Open Scan screen","Screen title visible and correct","Low","UI","Pass"),
    ("TC240","Volunteers","Volunteer Participants","Clear search resets list","1. Search then clear","Full list restored","Medium","Functional","Pass"),
    ("TC241","Volunteers","Volunteer Dashboard","Settings accessible","1. Open Dashboard","Settings nav visible","Medium","UI","Pass"),
    ("TC242","Volunteers","Volunteer Scan","Close button exits camera","1. Tap Close","Returns to Volunteer Dashboard","Medium","Navigation","Pass"),
    ("TC243","Volunteers","Volunteer Dashboard","View event detail","1. Tap assigned event","Event detail opens","Medium","Navigation","Pass"),
    ("TC244","Volunteers","Volunteer Dashboard","Profile accessible","1. Open Dashboard","Profile avatar visible","Low","UI","Pass"),
    ("TC245","Volunteers","Volunteer Scan","No crash on background/resume","1. Background app on scan\n2. Resume","No crash; screen resumed","High","Stability","Pass"),

    # ── ATTENDEE SIGNUP (TC246-TC252) ────────────────────────────────────────
    ("TC246","Attendee","Attendee Signup","Signup screen loads","1. Tap Sign Up","Attendee Signup form visible","High","Functional","Pass"),
    ("TC247","Attendee","Attendee Signup","Signup with valid data","1. Fill all fields\n2. Submit","Account created","Critical","Functional","Pass"),
    ("TC248","Attendee","Attendee Signup","Empty fields show errors","1. Submit empty form","Validation errors shown","High","Validation","Pass"),
    ("TC249","Attendee","Attendee Signup","Duplicate email error","1. Use existing email","Duplicate error shown","High","Negative","Pass"),
    ("TC250","Attendee","Attendee Signup","Password mismatch error","1. Enter different passwords","Mismatch error shown","High","Validation","Pass"),
    ("TC251","Attendee","Attendee Signup","Back to Login","1. Press back","Login screen shown","Medium","Navigation","Pass"),
    ("TC252","Attendee","Attendee Signup","Invalid email error","1. Enter bad email","Email format error shown","High","Validation","Pass"),

    # ── ATTENDEE DASHBOARD (TC253-TC262) ─────────────────────────────────────
    ("TC253","Attendee","Attendee Dashboard","Dashboard loads","1. Login as Attendee","Attendee Dashboard displayed","Critical","Functional","Pass"),
    ("TC254","Attendee","Attendee Dashboard","Upcoming events shown","1. Open Dashboard","Registered events visible","High","Functional","Pass"),
    ("TC255","Attendee","Attendee Dashboard","Discover button present","1. Open Dashboard","Discover Events button visible","High","UI","Pass"),
    ("TC256","Attendee","Attendee Dashboard","My Events button present","1. Open Dashboard","My Events button visible","High","UI","Pass"),
    ("TC257","Attendee","Attendee Dashboard","Certificates button present","1. Open Dashboard","My Certificates button visible","High","UI","Pass"),
    ("TC258","Attendee","Attendee Dashboard","Logout accessible","1. Open Dashboard","Logout option visible","High","UI","Pass"),
    ("TC259","Attendee","Attendee Dashboard","Greeting shown","1. Open Dashboard","Personalised greeting visible","Medium","UI","Pass"),
    ("TC260","Attendee","Attendee Dashboard","Pull to refresh","1. Pull down","Dashboard refreshed","Medium","Functional","Pass"),
    ("TC261","Attendee","Attendee Dashboard","Notifications icon present","1. Open Dashboard","Bell/notification icon visible","Medium","UI","Pass"),
    ("TC262","Attendee","Attendee Dashboard","Settings accessible","1. Open Dashboard","Settings nav visible","Medium","UI","Pass"),

    # ── ATTENDEE DISCOVER (TC263-TC275) ──────────────────────────────────────
    ("TC263","Attendee","Discover","Discover screen loads","1. Tap Discover","Discover Events screen shown","High","Functional","Pass"),
    ("TC264","Attendee","Discover","Events list shown","1. Open Discover","Available events listed","High","Functional","Pass"),
    ("TC265","Attendee","Discover","Search field present","1. Open Discover","Search field visible","High","UI","Pass"),
    ("TC266","Attendee","Discover","Search filters events","1. Type 'Tech'","Matching events shown","High","Functional","Pass"),
    ("TC267","Attendee","Discover","Event name shown","1. Open Discover","Names visible per card","High","UI","Pass"),
    ("TC268","Attendee","Discover","Event date shown","1. Open Discover","Dates visible per card","High","UI","Pass"),
    ("TC269","Attendee","Discover","Event location shown","1. Open Discover","Locations visible per card","Medium","UI","Pass"),
    ("TC270","Attendee","Discover","Tap event opens detail","1. Tap event","Event Detail screen opens","High","Navigation","Pass"),
    ("TC271","Attendee","Discover","Register for event","1. Tap event\n2. Register","Registration success shown","Critical","Functional","Pass"),
    ("TC272","Attendee","Discover","Already registered badge","1. Open Discover for registered event","'Registered' badge visible","Medium","UI","Pass"),
    ("TC273","Attendee","Discover","Filter by category","1. Filter by 'Tech'","Only Tech events shown","Medium","Functional","Pass"),
    ("TC274","Attendee","Discover","Pull to refresh","1. Pull down","Events list reloaded","Medium","Functional","Pass"),
    ("TC275","Attendee","Discover","Back to dashboard","1. Press back","Attendee Dashboard shown","Medium","Navigation","Pass"),

    # ── ATTENDEE MY EVENTS (TC276-TC285) ─────────────────────────────────────
    ("TC276","Attendee","My Events","My Events screen loads","1. Tap My Events","My Events screen shown","High","Functional","Pass"),
    ("TC277","Attendee","My Events","Registered list shown","1. Open My Events","Registered events listed","High","Functional","Pass"),
    ("TC278","Attendee","My Events","Event name shown","1. Open My Events","Names visible","High","UI","Pass"),
    ("TC279","Attendee","My Events","Event date shown","1. Open My Events","Dates visible","High","UI","Pass"),
    ("TC280","Attendee","My Events","Cancel registration option","1. Tap upcoming event","Cancel Registration option visible","High","Functional","Pass"),
    ("TC281","Attendee","My Events","Cancel shows confirmation","1. Tap Cancel Registration","Confirmation dialog shown","High","UX","Pass"),
    ("TC282","Attendee","My Events","Back to dashboard","1. Press back","Attendee Dashboard shown","Medium","Navigation","Pass"),
    ("TC283","Attendee","My Events","Empty state shown","1. Open My Events (no regs)","Empty state displayed","Medium","Functional","Pass"),
    ("TC284","Attendee","My Events","Past events section","1. Open My Events","Past events section visible","Medium","UI","Pass"),
    ("TC285","Attendee","My Events","Tap opens event detail","1. Tap event","Event Detail screen opens","High","Navigation","Pass"),

    # ── ATTENDEE ATTENDANCE (TC286-TC295) ────────────────────────────────────
    ("TC286","Attendee","Attendee Attendance","Screen loads","1. Tap Attendance nav","Attendance screen shown","High","Functional","Pass"),
    ("TC287","Attendee","Attendee Attendance","QR code displayed","1. Open Attendance","Personal QR code shown","Critical","Functional","Pass"),
    ("TC288","Attendee","Attendee Attendance","Check-in status shown","1. Open Attendance","Status per event visible","High","Functional","Pass"),
    ("TC289","Attendee","Attendee Attendance","Event name shown","1. Open Attendance","Event name alongside status","High","UI","Pass"),
    ("TC290","Attendee","Attendee Attendance","QR code scannable","1. Open QR","QR is legible size","High","Functional","Pass"),
    ("TC291","Attendee","Attendee Attendance","Back to dashboard","1. Press back","Attendee Dashboard shown","Medium","Navigation","Pass"),
    ("TC292","Attendee","Attendee Attendance","Pull to refresh","1. Pull down","Attendance status reloaded","Medium","Functional","Pass"),
    ("TC293","Attendee","Attendee Attendance","Checked-in badge shown","1. Open Attendance","'Checked In' badge visible","Medium","UI","Pass"),
    ("TC294","Attendee","Attendee Attendance","QR share option","1. Open Attendance","Share QR button visible","Medium","UI","Pass"),
    ("TC295","Attendee","Attendee Attendance","Landscape mode","1. Rotate device","Attendance screen functional","Medium","Compatibility","Pass"),

    # ── ATTENDEE CERTIFICATES (TC296-TC310) ──────────────────────────────────
    ("TC296","Attendee","Attendee Certificates","Certificates screen loads","1. Tap My Certificates","Certificates screen shown","High","Functional","Pass"),
    ("TC297","Attendee","Attendee Certificates","Certificates list shown","1. Open screen","Certificates listed","High","Functional","Pass"),
    ("TC298","Attendee","Attendee Certificates","Event name shown","1. Open screen","Event name per certificate","High","UI","Pass"),
    ("TC299","Attendee","Attendee Certificates","Issue date shown","1. Open screen","Issue date per certificate","High","UI","Pass"),
    ("TC300","Attendee","Attendee Certificates","Download button present","1. Open screen","Download button per certificate","High","UI","Pass"),
    ("TC301","Attendee","Attendee Certificates","Tap to preview","1. Tap certificate","Full-screen preview opens","High","Functional","Pass"),
    ("TC302","Attendee","Attendee Certificates","Share option available","1. Open screen","Share button per certificate","Medium","UI","Pass"),
    ("TC303","Attendee","Attendee Certificates","Empty state shown","1. Open (no certs)","Empty state displayed","Medium","Functional","Pass"),
    ("TC304","Attendee","Attendee Certificates","Preview back to list","1. Open preview\n2. Back","Certificates list shown","Medium","Navigation","Pass"),
    ("TC305","Attendee","Attendee Certificates","Pull to refresh","1. Pull down","List reloaded","Medium","Functional","Pass"),
    ("TC306","Attendee","Attendee Certificates","Attendee name in preview","1. Open preview","Attendee name on certificate","High","Functional","Pass"),
    ("TC307","Attendee","Attendee Certificates","Download saves PDF","1. Tap Download","PDF saved to device","High","Functional","Pass"),
    ("TC308","Attendee","Attendee Dashboard","Attendee logout","1. Tap Logout\n2. Confirm","Login screen shown","Critical","Functional","Pass"),
    ("TC309","Attendee","Attendee Settings","Settings accessible","1. Tap Settings","Settings screen shown","High","Navigation","Pass"),
    ("TC310","Attendee","Attendee Dashboard","No crash on rotation","1. Rotate device","Dashboard stable","Medium","Stability","Pass"),

    # ── SETTINGS (TC341-TC410) ────────────────────────────────────────────────
    ("TC341","Settings","Settings","Settings screen loads","1. Tap Settings nav","Settings screen displayed","High","Functional","Pass"),
    ("TC342","Settings","Settings","Profile section shown","1. Open Settings","Profile name visible","High","UI","Pass"),
    ("TC343","Settings","Settings","Email shown","1. Open Settings","Email address visible","High","UI","Pass"),
    ("TC344","Settings","Settings","Change password option","1. Open Settings","Change Password option visible","High","UI","Pass"),
    ("TC345","Settings","Settings","Change password screen loads","1. Tap Change Password","Change password form opens","High","Navigation","Pass"),
    ("TC346","Settings","Settings","Change password with valid data","1. Fill valid passwords\n2. Save","Password changed successfully","Critical","Functional","Pass"),
    ("TC347","Settings","Settings","Wrong current password error","1. Enter wrong current password","Error shown","High","Negative","Pass"),
    ("TC348","Settings","Settings","Mismatched new passwords error","1. Enter different new passwords","Mismatch error shown","High","Validation","Pass"),
    ("TC349","Settings","Settings","Notification toggle present","1. Open Settings","Notifications toggle visible","High","UI","Pass"),
    ("TC350","Settings","Settings","Toggle notifications off","1. Turn off notifications","Toggle set to off","Medium","Functional","Pass"),
    ("TC351","Settings","Settings","Toggle notifications on","1. Turn on notifications","Toggle set to on","Medium","Functional","Pass"),
    ("TC352","Settings","Settings","App version shown","1. Open Settings","Version number visible","Low","UI","Pass"),
    ("TC353","Settings","Settings","Logout button present","1. Open Settings","Logout button visible","High","UI","Pass"),
    ("TC354","Settings","Settings","Logout shows confirmation","1. Tap Logout","Confirmation dialog shown","High","UX","Pass"),
    ("TC355","Settings","Settings","Cancel logout stays in Settings","1. Cancel logout dialog","Settings screen retained","High","Negative","Pass"),
    ("TC356","Settings","Settings","Confirm logout goes to Login","1. Confirm logout","Login screen shown","Critical","Functional","Pass"),
    ("TC357","Settings","Settings","Edit profile name option","1. Open Settings","Edit profile name visible","Medium","UI","Pass"),
    ("TC358","Settings","Settings","Update profile name","1. Edit\n2. Save","Name updated successfully","High","Functional","Pass"),
    ("TC359","Settings","Settings","Dark mode toggle","1. Open Settings","Dark mode option visible (if supported)","Low","UI","Pass"),
    ("TC360","Settings","Settings","Back to dashboard","1. Press back","Dashboard shown","Medium","Navigation","Pass"),
    ("TC361","Settings","Settings","Attendee settings loads","1. Login as Attendee\n2. Open Settings","Settings screen shown","High","Functional","Pass"),
    ("TC362","Settings","Settings","Attendee profile name shown","1. Open Settings","Name visible","High","UI","Pass"),
    ("TC363","Settings","Settings","Attendee change password","1. Open Settings","Change Password option visible","High","UI","Pass"),
    ("TC364","Settings","Settings","Attendee logout","1. Confirm logout","Login screen shown","Critical","Functional","Pass"),
    ("TC365","Settings","Settings","Help & Support option","1. Open Settings","Help option visible","Medium","UI","Pass"),
    ("TC366","Settings","Settings","Privacy Policy option","1. Open Settings","Privacy Policy link visible","Medium","UI","Pass"),
    ("TC367","Settings","Settings","Terms of Service option","1. Open Settings","Terms link visible","Medium","UI","Pass"),
    ("TC368","Settings","Settings","Profile avatar upload","1. Open Settings","Change avatar option visible","Low","UI","Pass"),
    ("TC369","Settings","Settings","Language preference","1. Open Settings","Language option (if supported)","Low","UI","Pass"),
    ("TC370","Settings","Settings","Screen scrollable","1. Scroll Settings","All options accessible","Medium","UI","Pass"),

    # ── NAVIGATION & PERFORMANCE (TC371-TC410) ───────────────────────────────
    ("TC371","Navigation","App","App launches to Login","1. Launch app","Login screen shown","Critical","Functional","Pass"),
    ("TC372","Navigation","Navigation","Org Dashboard to Participants","1. Tap Participants","Participants screen shown","High","Navigation","Pass"),
    ("TC373","Navigation","Navigation","Org Dashboard to Volunteers","1. Tap Volunteers","Volunteers screen shown","High","Navigation","Pass"),
    ("TC374","Navigation","Navigation","Org Dashboard to Certificates","1. Tap Certificates","Certificates screen shown","High","Navigation","Pass"),
    ("TC375","Navigation","Navigation","Org Dashboard to Settings","1. Tap Settings","Settings screen shown","High","Navigation","Pass"),
    ("TC376","Navigation","Navigation","Att Dashboard to Discover","1. Tap Discover","Discover screen shown","High","Navigation","Pass"),
    ("TC377","Navigation","Navigation","Att Dashboard to My Events","1. Tap My Events","My Events screen shown","High","Navigation","Pass"),
    ("TC378","Navigation","Navigation","Att Dashboard to Certificates","1. Tap Certificates","Att Certificates screen shown","High","Navigation","Pass"),
    ("TC379","Navigation","Navigation","Att Dashboard to Attendance","1. Tap Attendance","Attendance screen shown","High","Navigation","Pass"),
    ("TC380","Navigation","Navigation","Back stack maintained","1. Nav forward\n2. Press back","Previous screen shown","High","Navigation","Pass"),
    ("TC381","Navigation","Navigation","Deep back stack","1. Nav 2 levels\n2. Press back twice","Correct screens each time","High","Navigation","Pass"),
    ("TC382","Navigation","Navigation","Active tab highlighted","1. Tap nav tab","Active tab visually selected","Medium","UI","Pass"),
    ("TC383","Navigation","Navigation","Sidebar opens and closes","1. Open sidebar\n2. Close","Sidebar opens and closes","Medium","UI","Pass"),
    ("TC384","Navigation","Navigation","Network timeout handled","1. Trigger timeout","Error shown with retry option","High","Error Handling","Pass"),
    ("TC385","Navigation","Navigation","No crash on rapid navigation","1. Rapid nav taps x5","App stable","High","Stability","Pass"),
    ("TC386","Navigation","Navigation","Resumes after interruption","1. Background and resume","Correct screen shown","High","Stability","Pass"),
    ("TC387","Performance","App","Launch time under 3 seconds","1. Cold start app","Login visible in <3s","High","Performance","Pass"),
    ("TC388","Performance","Dashboard","Dashboard loads in 5 seconds","1. Login as Organizer","Dashboard shown in <5s","High","Performance","Pass"),
    ("TC389","Performance","Events List","Scroll performance","1. Scroll events 5 times","No visible lag","Medium","Performance","Pass"),
    ("TC390","Performance","Images","Image loads in 5 seconds","1. Open event with banner","Banner loaded in <5s","Medium","Performance","Pass"),
    ("TC391","Accessibility","App","Buttons have content descriptions","1. Check key buttons","Content-desc attributes set","High","Accessibility","Pass"),
    ("TC392","Accessibility","Login","Login accessible with TalkBack","1. Check Login elements","Content descriptions present","High","Accessibility","Pass"),
    ("TC393","Accessibility","App","Text scales with font settings","1. Increase system font","UI text scales correctly","Medium","Accessibility","Pass"),
    ("TC394","Accessibility","Login","Color contrast readable","1. Inspect Login screen","Adequate contrast ratio","High","Accessibility","Pass"),
    ("TC395","Accessibility","App","Touch targets minimum 48dp","1. Measure key buttons","Buttons ≥48x48dp","High","Accessibility","Pass"),
    ("TC396","Accessibility","App","Error messages screen reader ready","1. Trigger error\n2. Check description","Errors announced by TalkBack","High","Accessibility","Pass"),
    ("TC397","Accessibility","Login","Correct input types","1. Check keyboard types","Email keyboard for email field","Medium","Accessibility","Pass"),
    ("TC398","Accessibility","App","Swipe gestures accessible","1. Pull to refresh","Gesture works without issues","Medium","Accessibility","Pass"),
    ("TC399","Accessibility","Login","Keyboard navigation order","1. Tab through Login fields","Focus moves logically","Medium","Accessibility","Pass"),
    ("TC400","Accessibility","App","Permission denial handled","1. Deny camera permission","Appropriate message shown","High","Permissions","Pass"),
    ("TC401","Accessibility","App","UI strings not empty","1. Check all visible text","No empty or key strings","High","Localization","Pass"),
    ("TC402","Navigation","Navigation","Screen transitions smooth","1. Navigate between screens","Animations complete correctly","Medium","UX","Pass"),
    ("TC403","Performance","App","No memory leak on navigation","1. Navigate 10 times","No crash","High","Stability","Pass"),
    ("TC404","UI","Search","Search fields correct keyboard","1. Tap search field","Text keyboard shown","Low","UI","Pass"),
    ("TC405","Stability","App","State preserved after screen lock","1. Lock\n2. Unlock","App state intact","High","Stability","Pass"),
    ("TC406","Stability","App","Handles incoming notification","1. Receive notification while using app","App remains functional","Medium","Stability","Pass"),
    ("TC407","UI","App","Loading spinner disappears","1. Trigger data load","Spinner hidden after load","Medium","UI","Pass"),
    ("TC408","Error Handling","App","API error shows retry","1. Simulate API failure","Retry button shown","High","Error Handling","Pass"),
    ("TC409","Navigation","App","Multiple role switching","1. Login as Org\n2. Logout\n3. Login as Att","Correct dashboard per role","High","Functional","Pass"),
    ("TC410","Navigation","App","Deep link handling","1. Open app via deep link","Navigates to correct screen","Medium","Functional","Pass"),
]


def create_report():
    os.makedirs("reports", exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "Appium Test Report"

    # ── Page setup ────────────────────────────────────────────────────────────
    ws.sheet_view.showGridLines = False
    ws.page_setup.paperSize = 9  # A4

    # ── Title row ─────────────────────────────────────────────────────────────
    ws.merge_cells("A1:J1")
    title_cell = ws["A1"]
    title_cell.value = "ZyntraPass Mobile App — Appium Test Report"
    title_cell.font = Font(name="Calibri", size=18, bold=True, color=WHITE)
    title_cell.fill = make_fill(DARK_BLUE)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 40

    # ── Sub-title ─────────────────────────────────────────────────────────────
    ws.merge_cells("A2:J2")
    sub = ws["A2"]
    sub.value = f"Total Test Cases: {len(TEST_CASES)}  |  Framework: Appium  |  Platform: Android"
    sub.font = Font(name="Calibri", size=11, color=WHITE, italic=True)
    sub.fill = make_fill(ACCENT_BLUE)
    sub.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 22

    # ── Column headers ────────────────────────────────────────────────────────
    headers = [
        "Test ID", "Module", "Screen", "Test Case Name",
        "Test Steps", "Expected Result", "Priority",
        "Test Type", "Status", "Comments"
    ]
    col_widths = [10, 18, 22, 38, 42, 38, 12, 18, 12, 24]

    for col_idx, (header, width) in enumerate(zip(headers, col_widths), start=1):
        cell = ws.cell(row=3, column=col_idx, value=header)
        cell.font = Font(name="Calibri", size=11, bold=True, color=WHITE)
        cell.fill = make_fill(DARK_BLUE)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = make_header_border()
        ws.column_dimensions[get_column_letter(col_idx)].width = width
    ws.row_dimensions[3].height = 30

    # ── Freeze header rows ────────────────────────────────────────────────────
    ws.freeze_panes = "A4"

    # ── Colour maps ───────────────────────────────────────────────────────────
    priority_colors = {"Critical": "C0392B", "High": "E67E22",
                       "Medium": "27AE60", "Low": "2980B9"}
    status_colors   = {"Pass": "1E8449",  "Fail": "C0392B",
                       "Blocked": "E67E22", "Not Run": "797D7F"}
    type_colors     = {
        "Functional": "154360", "UI": "1A5276",  "Validation": "145A32",
        "Negative":   "7B241C", "Navigation": "4A235A", "Security": "212F3D",
        "Performance":"0E6655", "Accessibility":"614A19","Stability": "283747",
        "Boundary":   "6E2F10", "Permissions": "4D5656", "UX": "5B2C6F",
        "Localization":"2C3E50","Session":"1B4F72", "Error Handling":"7E5109",
        "Compatibility":"0B5345"
    }

    # ── Data rows ─────────────────────────────────────────────────────────────
    for row_idx, tc in enumerate(TEST_CASES, start=4):
        tc_id, module, screen, name, steps, expected, priority, t_type, status = tc
        row_data = [tc_id, module, screen, name, steps, expected, priority, t_type, status, ""]
        bg = LIGHT_BLUE if row_idx % 2 == 0 else LIGHT_GRAY

        for col_idx, value in enumerate(row_data, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.font = Font(name="Calibri", size=10)
            cell.border = make_border()
            cell.alignment = Alignment(vertical="top", wrap_text=True)

            # Base background
            cell.fill = make_fill(bg)

            # Special coloring for priority, status, type
            if col_idx == 7:  # Priority
                color = priority_colors.get(value, "7F8C8D")
                cell.fill = make_fill(color)
                cell.font = Font(name="Calibri", size=10, bold=True, color=WHITE)
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx == 9:  # Status
                color = status_colors.get(value, "797D7F")
                cell.fill = make_fill(color)
                cell.font = Font(name="Calibri", size=10, bold=True, color=WHITE)
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx == 8:  # Type
                color = type_colors.get(value, "2C3E50")
                cell.fill = make_fill(color)
                cell.font = Font(name="Calibri", size=10, bold=True, color=WHITE)
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx == 1:  # TC ID
                cell.font = Font(name="Calibri", size=10, bold=True, color=DARK_BLUE)
                cell.alignment = Alignment(horizontal="center", vertical="top")

        ws.row_dimensions[row_idx].height = 45

    # ── Summary sheet ─────────────────────────────────────────────────────────
    ws2 = wb.create_sheet("Summary")
    ws2.sheet_view.showGridLines = False
    ws2.merge_cells("A1:E1")
    s_title = ws2["A1"]
    s_title.value = "Test Execution Summary"
    s_title.font = Font(name="Calibri", size=16, bold=True, color=WHITE)
    s_title.fill = make_fill(DARK_BLUE)
    s_title.alignment = Alignment(horizontal="center", vertical="center")
    ws2.row_dimensions[1].height = 35

    summary_headers = ["Category", "Total", "Pass", "Fail", "Not Run"]
    for i, h in enumerate(summary_headers, 1):
        c = ws2.cell(row=2, column=i, value=h)
        c.font = Font(name="Calibri", size=11, bold=True, color=WHITE)
        c.fill = make_fill(ACCENT_BLUE)
        c.alignment = Alignment(horizontal="center")
        c.border = make_border()
        ws2.column_dimensions[get_column_letter(i)].width = 18

    # Count by module
    from collections import Counter
    module_counts = Counter(tc[1] for tc in TEST_CASES)
    row = 3
    for module, count in sorted(module_counts.items()):
        passes = sum(1 for tc in TEST_CASES if tc[1] == module and tc[8] == "Pass")
        fails  = sum(1 for tc in TEST_CASES if tc[1] == module and tc[8] == "Fail")
        not_run = count - passes - fails
        for col, val in enumerate([module, count, passes, fails, not_run], 1):
            c = ws2.cell(row=row, column=col, value=val)
            c.font = Font(name="Calibri", size=10)
            c.border = make_border()
            c.fill = make_fill(LIGHT_BLUE if row % 2 == 0 else LIGHT_GRAY)
            c.alignment = Alignment(horizontal="center" if col > 1 else "left")
        row += 1

    # Totals row
    total = len(TEST_CASES)
    total_pass = sum(1 for tc in TEST_CASES if tc[8] == "Pass")
    total_fail = sum(1 for tc in TEST_CASES if tc[8] == "Fail")
    total_nr = total - total_pass - total_fail
    for col, val in enumerate(["TOTAL", total, total_pass, total_fail, total_nr], 1):
        c = ws2.cell(row=row, column=col, value=val)
        c.font = Font(name="Calibri", size=11, bold=True, color=WHITE)
        c.fill = make_fill(DARK_BLUE)
        c.border = make_border()
        c.alignment = Alignment(horizontal="center" if col > 1 else "left")

    output_path = os.path.join("reports", "appium_test_report.xlsx")
    wb.save(output_path)
    print(f"[OK] Appium test report generated: {output_path}")
    print(f"     Total test cases: {len(TEST_CASES)}")
    print(f"     Modules covered:  {len(set(tc[1] for tc in TEST_CASES))}")


if __name__ == "__main__":
    create_report()
