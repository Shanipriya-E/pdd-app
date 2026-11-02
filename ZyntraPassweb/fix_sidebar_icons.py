import re

files = [
    'dashboard.html', 
    'events.html', 
    'participants.html', 
    'live.html', 
    'volunteers.html', 
    'certificates.html', 
    'settings.html'
]

sidebar_template = '''<div class="sidebar-menu">
        <a href="dashboard.html" class="sidebar-item"><span>\U0001f3e0</span> Dashboard</a>
        <a href="events.html" class="sidebar-item"><span>\U0001f4c5</span> Events</a>
        <a href="participants.html" class="sidebar-item"><span>\U0001f465</span> Participants</a>
        <a href="live.html" class="sidebar-item"><span>\U0001f4e1</span> Live Attendance</a>
        <a href="volunteers.html" class="sidebar-item"><span>\U0001f91d</span> Volunteers</a>
        <a href="certificates.html" class="sidebar-item"><span>\U0001f4dc</span> Certificates</a>
        <a href="settings.html" class="sidebar-item"><span>\u2699\ufe0f</span> Settings</a>
    </div>'''

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        content = re.sub(r'<div class="sidebar-menu">.*?</div>', sidebar_template, content, flags=re.DOTALL)
        
        if f == 'dashboard.html':
            content = content.replace('href="dashboard.html" class="sidebar-item"', 'href="dashboard.html" class="sidebar-item active"')
        elif f == 'events.html':
            content = content.replace('href="events.html" class="sidebar-item"', 'href="events.html" class="sidebar-item active"')
        elif f == 'participants.html':
            content = content.replace('href="participants.html" class="sidebar-item"', 'href="participants.html" class="sidebar-item active"')
        elif f == 'live.html':
            content = content.replace('href="live.html" class="sidebar-item"', 'href="live.html" class="sidebar-item active"')
        elif f == 'volunteers.html':
            content = content.replace('href="volunteers.html" class="sidebar-item"', 'href="volunteers.html" class="sidebar-item active"')
        elif f == 'certificates.html':
            content = content.replace('href="certificates.html" class="sidebar-item"', 'href="certificates.html" class="sidebar-item active"')
        elif f == 'settings.html':
            content = content.replace('href="settings.html" class="sidebar-item"', 'href="settings.html" class="sidebar-item active"')

        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
            
        print("Fixed " + f)
    except Exception as e:
        print("Error processing " + f + ": " + str(e))

