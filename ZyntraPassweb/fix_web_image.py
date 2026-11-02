import os

filepath = 'c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/attendee_event_detail.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix banner-placeholder garbled text
import re
content = re.sub(r'<div class="banner-placeholder">.*?</div', '<div class="banner-placeholder">🖼️</div', content)

# Fix Javascript logic
old_js = """        // Banner
        if (ev.banner_image_url) {
            document.getElementById('bannerContainer').innerHTML = `<img src="${ev.banner_image_url}" 
class="event-banner" alt="Banner">`;
        }"""

new_js = """        // Banner
        if (ev.banner_image_url && ev.banner_image_url !== 'null') {
            document.getElementById('bannerContainer').innerHTML = `<img src="${ev.banner_image_url}" class="event-banner" alt="Banner">`;
        } else {
            document.getElementById('bannerContainer').innerHTML = `<img src="https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1200" class="event-banner" alt="Banner">`;
        }"""

# Since newlines might not match exactly, we can use a simpler replacement
content = content.replace("if (ev.banner_image_url) {\n            document.getElementById('bannerContainer').innerHTML = `<img src=\"${ev.banner_image_url}\" \nclass=\"event-banner\" alt=\"Banner\">`;\n        }", new_js)

# Wait, let's just use regex for JS
content = re.sub(r'if\s*\(ev\.banner_image_url\)\s*\{\s*document\.getElementById\(\'bannerContainer\'\)\.innerHTML\s*=\s*`<img src="\$\{ev\.banner_image_url\}"[^>]*>`;\s*\}', new_js, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed web app image logic")
