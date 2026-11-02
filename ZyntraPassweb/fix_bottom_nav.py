# -*- coding: utf-8 -*-
import re

files = [
    'attendee_dashboard.html', 
    'attendee_discover.html', 
    'attendee_my_events.html', 
    'attendee_attendance.html', 
    'attendee_settings.html',
    'attendee_certificates.html'
]

bottom_template = r'''<div class="bottom-nav">
    <a href="attendee_dashboard.html" class="nav-item">
        <span class="nav-icon">🏠</span><span>Dashboard</span>
    </a>
    <a href="attendee_discover.html" class="nav-item">
        <span class="nav-icon">🔍</span><span>Discover</span>
    </a>
    <a href="attendee_my_events.html" class="nav-item">
        <span class="nav-icon">📅</span><span>Events</span>
    </a>
    <a href="attendee_certificates.html" class="nav-item">
        <span class="nav-icon">📜</span><span>Certs</span>
    </a>
</div>'''

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        if '<div class="bottom-nav">' in content:
            content = re.sub(r'<div class="bottom-nav">.*?</div>', bottom_template, content, flags=re.DOTALL)
        else:
            # Inject before </body> if missing
            content = content.replace('</body>', '<!-- Bottom Nav -->\n' + bottom_template + '\n</body>')
        
        # Adjust active state for bottom nav
        if f == 'attendee_dashboard.html':
            content = content.replace('href="attendee_dashboard.html" class="nav-item"', 'href="attendee_dashboard.html" class="nav-item active"')
        elif f == 'attendee_discover.html':
            content = content.replace('href="attendee_discover.html" class="nav-item"', 'href="attendee_discover.html" class="nav-item active"')
        elif f == 'attendee_my_events.html':
            content = content.replace('href="attendee_my_events.html" class="nav-item"', 'href="attendee_my_events.html" class="nav-item active"')
        elif f == 'attendee_certificates.html':
            content = content.replace('href="attendee_certificates.html" class="nav-item"', 'href="attendee_certificates.html" class="nav-item active"')

        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
            
        print("Updated bottom nav in " + f)
    except Exception as e:
        print("Error processing " + f + ": " + str(e))

