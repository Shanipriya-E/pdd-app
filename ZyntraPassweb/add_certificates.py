import re

files = ['dashboard.html', 'events.html', 'participants.html', 'live.html', 'volunteers.html', 'settings.html']

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        if 'Certificates' not in content:
            content = content.replace(
                '<a href="settings.html" class="sidebar-item',
                '<a href="#" class="sidebar-item"><span>??</span> Certificates</a>\n        <a href="settings.html" class="sidebar-item'
            )
            
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Added certificates back to {f}")
    except Exception as e:
        print(f"Error in {f}: {e}")
