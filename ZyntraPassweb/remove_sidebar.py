import os, re
files = ['dashboard.html', 'events.html', 'participants.html', 'live.html', 'volunteers.html', 'settings.html']
for f in files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remove Analytics, Security, and Reports links
        content = re.sub(r'<a href="#" class="sidebar-item"><span>??</span> Analytics</a>\s*', '', content)
        content = re.sub(r'<a href="#" class="sidebar-item"><span>???</span> Security</a>\s*', '', content)
        content = re.sub(r'<a href="#" class="sidebar-item"><span>??</span> Reports</a>\s*', '', content)
        
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
print("Removed sidebar items")
