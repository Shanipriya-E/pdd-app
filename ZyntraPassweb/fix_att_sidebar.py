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

sidebar_template = r'''<div class="sidebar-menu">
            <a href="attendee_dashboard.html" class="sidebar-item"><span>🏠</span> Dashboard</a>
            <a href="attendee_discover.html" class="sidebar-item"><span>🔍</span> Discover</a>
            <a href="attendee_my_events.html" class="sidebar-item"><span>📅</span> My Events</a>
            <a href="attendee_attendance.html" class="sidebar-item"><span>📡</span> Attendance</a>
            <a href="attendee_certificates.html" class="sidebar-item"><span>📜</span> Certificates</a>
            <a href="attendee_settings.html" class="sidebar-item"><span>⚙️</span> Settings</a>
        </div>'''

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        content = re.sub(r'<div class="sidebar-menu">.*?</div>', sidebar_template, content, flags=re.DOTALL)
        
        # Adjust active state
        if f == 'attendee_dashboard.html':
            content = content.replace('href="attendee_dashboard.html" class="sidebar-item"', 'href="attendee_dashboard.html" class="sidebar-item active"')
        elif f == 'attendee_discover.html':
            content = content.replace('href="attendee_discover.html" class="sidebar-item"', 'href="attendee_discover.html" class="sidebar-item active"')
        elif f == 'attendee_my_events.html':
            content = content.replace('href="attendee_my_events.html" class="sidebar-item"', 'href="attendee_my_events.html" class="sidebar-item active"')
        elif f == 'attendee_attendance.html':
            content = content.replace('href="attendee_attendance.html" class="sidebar-item"', 'href="attendee_attendance.html" class="sidebar-item active"')
        elif f == 'attendee_certificates.html':
            content = content.replace('href="attendee_certificates.html" class="sidebar-item"', 'href="attendee_certificates.html" class="sidebar-item active"')
        elif f == 'attendee_settings.html':
            content = content.replace('href="attendee_settings.html" class="sidebar-item"', 'href="attendee_settings.html" class="sidebar-item active"')

        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
            
        print("Fixed " + f)
    except Exception as e:
        print("Error processing " + f + ": " + str(e))

