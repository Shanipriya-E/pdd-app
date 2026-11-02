import os

files = {
    'c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/attendee_my_events.html': 'attendee_my_events.html',
    'c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/attendee_certificates.html': 'attendee_certificates.html',
    'c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/attendee_settings.html': 'attendee_settings.html',
    'c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/attendee_discover.html': 'attendee_discover.html',
}

for fp, active_page in files.items():
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if attendance already exists between events and certs in nav
    nav_start = content.find('bottom-nav')
    nav_end = content.find('</div>', nav_start)
    nav_content = content[nav_start:nav_end]
    
    if 'attendee_attendance.html' in nav_content:
        print(f"Already has attendance link: {fp}")
        continue
    
    # Find the certs link and insert attendance before it
    old_certs = '    <a href="attendee_certificates.html" class="nav-item">'
    new_att_plus_certs = '    <a href="attendee_attendance.html" class="nav-item">\n        <span class="nav-icon">📡</span><span>Attendance</span>\n    </a>\n    <a href="attendee_certificates.html" class="nav-item">'
    
    if old_certs in content:
        content = content.replace(old_certs, new_att_plus_certs, 1)
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {fp}")
    else:
        print(f"Could not find certs link in: {fp}")

print("Done!")
