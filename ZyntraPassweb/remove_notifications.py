import re
files = ['c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/settings.html', 'c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/attendee_settings.html']
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Remove the remaining notification content
    pattern = r'<!-- Removed tab-notifications -->\s*<div class="settings-card">\s*<h2 class="card-title">Notifications</h2>\s*<p class="card-desc">Notification preferences will be available in the next update.</p>\s*</div>\s*</div>'
    content = re.sub(pattern, '', content)
    
    # Just in case it wasn't replaced properly before
    pattern2 = r'<div class="tab-content" id="tab-notifications">\s*<div class="settings-card">\s*<h2 class="card-title">Notifications</h2>\s*<p class="card-desc">Notification preferences will be available in the next update.</p>\s*</div>\s*</div>'
    content = re.sub(pattern2, '', content)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
print("Removed Notifications box")
