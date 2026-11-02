import re

files = ['dashboard.html', 'events.html', 'participants.html', 'live.html', 'volunteers.html', 'settings.html']

sidebar_new = '''<div class="sidebar-menu">
        <a href="dashboard.html" class="sidebar-item"><span>??</span> Dashboard</a>
        <a href="events.html" class="sidebar-item"><span>??</span> Events</a>
        <a href="participants.html" class="sidebar-item"><span>??</span> Participants</a>
        <a href="live.html" class="sidebar-item"><span>??</span> Live Attendance</a>
        <a href="volunteers.html" class="sidebar-item"><span>??</span> Volunteers</a>
        <a href="settings.html" class="sidebar-item"><span>??</span> Settings</a>
    </div>'''

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # We need to make sure we set the active class correctly if the old one had it.
        # But for now let's just replace the whole thing, then fix the active state based on filename
        
        content = re.sub(r'<div class="sidebar-menu">.*?</div>', sidebar_new, content, flags=re.DOTALL)
        
        # Re-add 'active' class to the correct item
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
        elif f == 'settings.html':
            content = content.replace('href="settings.html" class="sidebar-item"', 'href="settings.html" class="sidebar-item active"')
            
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Fixed {f}")
    except Exception as e:
        print(f"Error in {f}: {e}")
