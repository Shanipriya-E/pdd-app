import os, re
files = ['attendee_dashboard.html', 'attendee_my_events.html', 'attendee_discover.html', 'attendee_attendance.html']
for f in files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Replace the Settings link in the sidebar
        content = re.sub(r'<a href="#" class="sidebar-item"><span>(.*?)</span> Settings</a>', r'<a href="attendee_settings.html" class="sidebar-item"><span>\1</span> Settings</a>', content)
        
        # Replace the Settings link in the bottom nav if it exists
        content = re.sub(r'<a href="#" class="nav-item"><span class="nav-icon">(.*?)</span><span>Settings</span></a>', r'<a href="attendee_settings.html" class="nav-item"><span class="nav-icon">\1</span><span>Settings</span></a>', content)
        
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
print("Updated links")
