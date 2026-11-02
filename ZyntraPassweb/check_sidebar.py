import re

files = ['dashboard.html', 'events.html', 'participants.html', 'live.html', 'volunteers.html', 'settings.html']

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    match = re.search(r'<div class="sidebar-menu">.*?</div>', content, re.DOTALL)
    if match:
        print(f + ":")
        print(match.group(0))
        print("-" * 40)
