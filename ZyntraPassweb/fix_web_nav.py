import os

# Files to fix - add Attendance link between Events and Certs in bottom nav
files = [
    'c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/attendee_dashboard.html',
    'c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/attendee_discover.html',
    'c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/attendee_my_events.html',
    'c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/attendee_certificates.html',
]

OLD_NAV = """    <a href="attendee_my_events.html" class="nav-item"""
NEW_NAV_EXTRA = """    <a href="attendee_attendance.html" class="nav-item"""

for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'attendee_attendance.html' in content and 'nav-item' in content.split('attendee_attendance.html')[0].split('bottom-nav')[-1]:
        print(f"Already has attendance link in nav: {fp}")
        continue

    # We insert Attendance nav item BEFORE the Certs link
    OLD_CERTS_LINK = '    <a href="attendee_certificates.html" class="nav-item">'
    NEW_ATTENDANCE_PLUS_CERTS = '    <a href="attendee_attendance.html" class="nav-item">\n        <span class="nav-icon">📡</span><span>Attendance</span>\n    </a>\n    <a href="attendee_certificates.html" class="nav-item">'
    
    if OLD_CERTS_LINK in content and 'attendee_attendance.html' not in content.split('bottom-nav')[1].split('</div>')[0]:
        content = content.replace(OLD_CERTS_LINK, NEW_ATTENDANCE_PLUS_CERTS, 1)
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added Attendance link to bottom nav in: {fp}")
    else:
        print(f"Skipped (already has or couldn't find insertion point): {fp}")

print("Done!")
